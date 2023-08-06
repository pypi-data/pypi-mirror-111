from typing import Optional, List, Dict, Union, Any
import torch

from . import ConfigMetaClass


class SystemConfig(metaclass=ConfigMetaClass):
    # exp stores the value of --exp key argument passed to train.py in module-like representation - [exp_group.]exp
    exp: Optional[str] = None
    # exp_path stores the same value represented as a relative config path - [exp_group/]exp
    exp_path: Optional[str] = None

    # DATASETS

    # subfolder where input datasets are stored
    dataset_path = 'datasets'
    # subfolder for cached preprocessing data
    data_path = 'data'
    # train and validation datasets are separated beforehand
    use_ready_valid_split = False

    # subfolder where processed storages are saved
    storage_path = 'storage'
    # ignore and rewrite processed storages if they already exist
    rewrite_storage = False
    # filename separator for multi-worker datasets
    storage_file_sep = '_'
    # storage file extension
    hdf_ext = '.h5'
    # internal storage value for naming scalars got by splitting vector values elementwise
    storage_sep = '||'
    # base key used for IO operations with HDF files
    hdf_key = 'df'

    # LOGGING & CHECKPOINTS PATHS

    # path for logs to be saved to
    logs_path = 'logs'
    # name of logs subfolder for the experiment - if set to None will be same as experiment name
    logs_name: Optional[str] = None
    # log file name
    logs_file = 'run.log'
    # model path
    model_path: Optional[str] = None
    # checkpoint folder name
    checkpoints_folder = 'checkpoints'
    # logging format
    log_format = '%(levelname)s - %(module)s:%(funcName)s:%(lineno)s - %(asctime)s - %(message)s'
    date_format = '%y-%m-%d'
    time_format = '%H-%M-%S'
    log_time_format = f'{date_format}:{time_format}'

    # LOGGING

    train_metrics_freq = 1
    train_log_freq = 64
    val_log_freq = 1024
    checkpoint_step_freq: Optional[int] = None
    checkpoint_epoch_freq = 1

    pickle_protocol = 3

    # TASKS

    tasks: List[str] = ['main']

    weighted_tasks: List[str] = []

    # TRAINING

    batch_size = 1
    world_batch_size = 1
    total_size: Optional[int] = None
    epochs = 1

    use_amp = False
    amp_opt_level: Optional[str] = None
    amp_max_loss_scale: float = 2 ** 8

    optimizer_kwargs: Dict[str, Any] = {}
    lr = 0.001

    use_gradient_checkpointing = False

    skip_validation = False
    validate_at_start = True
    val_size = 0.025

    # DATA PREPARATION

    shuffle_samples = True

    multitask_inputs: List[str] = []

    # padding lengths for sequential inputs
    pad_len = 128

    dataset_coeffs = {}

    # DEVICES

    devices: Union[List[str], List[torch.device]] = ['cpu']
    device = devices[0]
    parallel_devices: List[torch.device] = None
    gpus_per_model = 1
    distributed = False

    distributed_type = 'ddp'

    # additional config for 'ddp'
    find_unused_parameters = True
    # additional config for 'apex'
    apex_max_loss_scale = 2. ** 8

    # RESTORING FROM CHECKPOINT

    restore = False
    restore_epoch = None
    restore_from = None
    restore_step = None

    # MULTINODE TRAINING

    node_rank: Optional[int] = None
    num_nodes: Optional[int] = None

    num_gpus = 1
    world_size = 1
    init_method = 'env://'

    master_addr = 'localhost'
    master_port = 8000

    @classmethod
    def init(cls):
        if isinstance(cls.devices, str):
            cls.devices = [cls.devices]

        if 'cpu' in cls.devices and cls.use_amp:
            raise ValueError(
                'Apex amp is only compatible with gpu devices, modify either Config.use_amp or Config.devices')

        cls.devices = [torch.device(device) for device in cls.devices]
        cls.device = cls.devices[0]

        if len(cls.tasks) == 1:
            cls.task = cls.tasks[0]

        if cls.total_size is None:
            cls.total_size = cls.batch_size

        if cls.total_size % cls.batch_size:
            raise ValueError('If set, Config.total_size should be a multiple of Config.batch_size')

        if cls.skip_validation:
            cls.val_log_freq = None
            cls.validate_at_start = False

        if cls.train_log_freq % cls.train_metrics_freq:
            raise ValueError('Config.train_log_freq should be a multiple of Config.train_metrics_freq')

        if cls.use_amp and (not hasattr(cls, 'amp_opt_level') or cls.amp_opt_level not in 'O0, O1, O2, O3'):
            raise ValueError('When using apex amp, Config.amp_opt_level should be set to one of "O0", "O1", "O2", "O3"')

        if cls.gpus_per_model > len(cls.devices):
            raise ValueError('Amount of devices set in Config.device is smaller than Config.gpus_per_model')

        cls.distributed = (len(cls.devices) > cls.gpus_per_model)

        if cls.distributed:
            cls.num_gpus = len(cls.devices)
            cls.parallel_devices = cls.devices
            cls.devices = [torch.device('cpu')]
            cls.device = cls.devices[0]
            cls.world_size = cls.num_gpus // cls.gpus_per_model
            assert cls.world_size > 0

            cls.world_batch_size = cls.batch_size * cls.world_size
            cls.total_size = cls.total_size * cls.world_size

            if cls.distributed_type == 'ddp' and not hasattr(cls, 'find_unused_parameters'):
                cls.find_unused_parameters = True

            if cls.distributed_type == 'ddp' and cls.use_amp and cls.amp_opt_level == 'O2':
                raise ValueError("Apex amp opt_level O2 isn't compatible with pytorch.distributed DDP")

            if cls.distributed_type == 'apex' and cls.gpus_per_model > 1:
                raise ValueError('Apex DDP supports only single-device models')

            if cls.node_rank is not None:
                if cls.num_nodes is None:
                    raise ValueError('When passing node_rank, num_nodes should be also set')
                cls.init_method = f'{cls.master_addr}:{cls.master_port}'
                cls.world_size *= cls.num_nodes
