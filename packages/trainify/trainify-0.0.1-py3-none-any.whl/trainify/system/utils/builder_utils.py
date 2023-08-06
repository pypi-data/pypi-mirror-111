from typing import Tuple, Dict, Optional
import os
from shutil import copyfile
import logging
import pandas as pd
import tqdm
import torch

from trainify.preparators import BasePreparator, Preparators, Cacher
from .samplers import StorageSampler
from .dataloaders import SingleTaskLoader
from .checkpointer import Checkpointer

from trainify.configs import SystemConfig, Components


def prepare_dataset(
        preparators: Preparators, dataset: Optional[pd.DataFrame] = None,
        meta: Optional[dict] = None, is_train: Optional[bool] = None) -> Tuple[pd.DataFrame, dict]:
    if meta is None:
        meta = {}
    if is_train is not None:
        meta['is_train'] = is_train
    if not preparators:
        return dataset, meta
    if isinstance(preparators, BasePreparator):
        return preparators.prepare(dataset, meta)
    elif isinstance(preparators, list):
        for ind, sub_prep in reversed(list(enumerate(preparators))):
            if isinstance(sub_prep, Cacher) and sub_prep.ready():
                try:
                    dataset, meta = sub_prep.prepare(dataset, meta)
                    preparators = preparators[ind + 1:]
                    break
                except Exception as e:
                    print(e)
                    sub_prep.rewrite = True
        for sub_prep in preparators:
            dataset, meta = prepare_dataset(sub_prep, dataset, meta)
    elif isinstance(preparators, tuple):
        datasets = []
        metas = []
        for sub_prep in preparators:
            new_dataset, new_meta = prepare_dataset(sub_prep, dataset, meta)
            datasets.append(new_dataset)
            metas.append(new_meta)
        dataset = pd.concat(datasets)
        for new_meta in metas:
            meta.update(new_meta)
    else:
        raise ValueError(
            f'type should be instance or nested list / dict of BasePreparator, received {type(preparators)}')

    if not isinstance(dataset, pd.DataFrame):
        raise ValueError(f'preparators should have returned pandas DataFrame, got {type(dataset)} instead')
    return dataset, meta


def split_dataset(inputs_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    bsz = SystemConfig.world_batch_size
    val_amount = int(round(len(inputs_df) * SystemConfig.val_size))
    val_amount = min(len(inputs_df) - bsz, max(val_amount, bsz))
    val_amount = val_amount // bsz * bsz
    train_amount = (len(inputs_df) - val_amount) // bsz * bsz
    return inputs_df[:train_amount].reset_index(drop=True), inputs_df[-val_amount:].reset_index(drop=True)


def convert_df_fields(df: pd.DataFrame) -> pd.DataFrame:
    from operator import itemgetter
    for column in list(df.columns):
        logging.info(f'Processing {column} column')
        sample_value = df.loc[0, column]
        if not hasattr(sample_value, '__len__'):
            continue
        length = len(sample_value)
        sep = '||'
        for ind in tqdm.trange(length):
            df[f'{column}{sep}{ind}'] = df[column].apply(itemgetter(ind))

        df = df.drop(columns=[column])
    return df


def init_logging(logs_path: str):
    os.makedirs(logs_path)
    copyfile(os.path.join('configs', f'{SystemConfig.exp_path}.py'), os.path.join(logs_path, 'configs.py'))
    logs_file_path = os.path.join(logs_path, SystemConfig.logs_file)
    logging.basicConfig(
        level=logging.INFO, format=SystemConfig.log_format, datefmt=SystemConfig.log_time_format,
        handlers=[logging.FileHandler(logs_file_path), logging.StreamHandler()])


def create_checkpointer(logs_path: str) -> Checkpointer:
    checkpoints_path = os.path.join(logs_path, SystemConfig.checkpoints_folder)
    os.makedirs(checkpoints_path)

    checkpointer = Checkpointer(checkpoints_path)
    logging.info(f'Checkpointer initialized at {checkpoints_path}')
    return checkpointer


def hdf_save(dataset: pd.DataFrame, filename: str):
    key = SystemConfig.hdf_key
    dataset.to_hdf(filename, key=key, mode='w', format='table')
    with pd.HDFStore(filename, mode='a') as store:
        store.get_storer(key).attrs.len = len(dataset)


def save_dataset(dataset: pd.DataFrame, filename: str):
    dataset = convert_df_fields(dataset)
    if SystemConfig.shuffle_samples:
        dataset = dataset.sample(frac=1).reset_index(drop=True)
    extension = SystemConfig.hdf_ext
    bsz = SystemConfig.batch_size
    world_bsz = SystemConfig.world_batch_size
    if SystemConfig.distributed:
        world_size = SystemConfig.world_size
        for rank in range(world_size):
            worker_indices = []
            for ind in range(0, (len(dataset) // world_bsz) * world_bsz, world_bsz):
                worker_indices += list(range(ind + rank * bsz, ind + (rank + 1) * bsz))
            worker_filename = f'{filename}{SystemConfig.storage_file_sep}{rank}{extension}'
            worker_dataset = dataset.iloc[worker_indices]
            hdf_save(worker_dataset, worker_filename)
    else:
        filename = filename + extension
        hdf_save(dataset, filename)


def prepare_data() -> Tuple[SingleTaskLoader, Optional[Dict[str, SingleTaskLoader]]]:
    preparators = Components.preparators
    samplers = {}

    for task in SystemConfig.tasks:
        logging.info(f'Preparing {task} data')
        path = os.path.join(SystemConfig.data_path, SystemConfig.storage_path, task)
        train_fn = os.path.join(path, 'train' if not SystemConfig.skip_validation else 'train_all')
        val_fn = os.path.join(path, 'val')
        if SystemConfig.rewrite_storage or not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            if SystemConfig.use_ready_valid_split:
                train_dataset, _ = prepare_dataset(preparators[task], is_train=True)
                val_dataset, _ = (prepare_dataset(preparators[task], is_train=False) if not SystemConfig.skip_validation
                                  else (None, None))
                for dataset, part in ((train_dataset, 'train'), (val_dataset, 'validation')):
                    if dataset is not None and len(dataset) < SystemConfig.world_batch_size:
                        raise ValueError(f'Processed {part} dataset is shorter than 1 batch, '
                                         f'decrease batch size or increase data amount')
            else:
                processed_dataset, _ = prepare_dataset(preparators[task])
                if len(processed_dataset) < 2 * SystemConfig.world_batch_size:
                    raise ValueError('Processed dataset is shorter than 2 batches, '
                                     'decrease batch size or increase data amount')
                train_dataset, val_dataset = (split_dataset(processed_dataset) if not SystemConfig.skip_validation
                                              else (processed_dataset, None))

            save_dataset(train_dataset, train_fn)
            if val_dataset is not None:
                save_dataset(val_dataset, val_fn)
        samplers[task] = StorageSampler(train_fn), StorageSampler(val_fn) if not SystemConfig.skip_validation else None
        logging.info(f'Prepared {task} data')

    # Temporarily works only for single task, refactor in future
    assert len(SystemConfig.tasks) == 1
    task = SystemConfig.tasks[0]
    train_dataloader = Components.dataloader(samplers[task][0])
    val_dataloaders = {task: Components.dataloader(samplers[task][1])} if not SystemConfig.skip_validation else None
    return train_dataloader, val_dataloaders


def create_model(meta: Optional[dict] = None) -> torch.nn.Module:
    model_cls = Components.model
    model = model_cls.from_pretrained(SystemConfig.model_path) if hasattr(model_cls, 'from_pretrained') else model_cls()

    if meta and hasattr(model, 'post_init'):
        model.post_init(**meta)

    if not SystemConfig.distributed:
        if hasattr(model, 'to_devices_'):
            model.to_devices_(SystemConfig.devices)
        elif SystemConfig.gpus_per_model == 1:
            model = model.to(SystemConfig.devices[0])
        else:
            raise ValueError('multi-gpu models should have to_devices_(devices) method defined')

    logging.info('Model created')
    return model


def create_optimizer(model: torch.nn.Module) -> Components.optimizer:
    optimizer = Components.optimizer(
        model.optimizer_parameters() if hasattr(model, 'optimizer_parameters')
        else model.parameters(), lr=SystemConfig.lr, **SystemConfig.optimizer_kwargs)
    if SystemConfig.use_amp and not SystemConfig.distributed:
        import apex
        model, optimizer = apex.amp.initialize(
            model, optimizer, opt_level=SystemConfig.amp_opt_level,
            max_loss_scale=SystemConfig.amp_max_loss_scale)
    logging.info('Optimizer created')
    return optimizer
