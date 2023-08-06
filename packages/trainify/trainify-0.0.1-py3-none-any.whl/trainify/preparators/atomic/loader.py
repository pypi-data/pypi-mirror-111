from typing import Optional, Tuple
import os
import logging
import pickle as pkl
import pandas as pd

from . import BasePreparator

from trainify.configs import SystemConfig


class Loader(BasePreparator):
    """
    base class for loading datasets. may be used as it is, or extended to support wider variety of formats
    """
    mode_exts = {'hdf': ('h5', 'hdf', 'hdf5'), 'pkl': ('pkl', 'pickle', 'pt')}
    ext_to_mode = {ext: mode for mode, exts in mode_exts.items() for ext in exts}
    modes = tuple(mode_exts.keys())
    key = SystemConfig.hdf_key

    base_path = SystemConfig.dataset_path

    def __init__(self, filename: str, meta_filename: Optional[str] = None, mode: str = None):
        if meta_filename is not None:
            logging.warning('using meta_filename parameter should be avoided, reserved mostly for debugging purposes')
        if mode is None:
            if '.' in filename:
                mode = self.ext_to_mode.get(filename.rsplit('.', maxsplit=1)[-1], None)
            if mode is None:
                mode = 'pkl'
                logging.debug("Loader mode couldn't be recognized by filename, setting to pickle")
        else:
            if '.' in filename:
                ext = filename.rsplit('.', maxsplit=1)[-1]
                if self.ext_to_mode.get(ext, mode) != mode:
                    raise ValueError(f'Loader mode {mode} is conflicting with extension {ext}')
            else:
                filename = f'{filename}.{mode}'
        assert mode in self.modes, f'mode is {mode}, available: {self.modes}'

        filename = os.path.join(self.base_path, filename)
        if SystemConfig.use_ready_valid_split:
            split_fn = filename.rsplit('.', maxsplit=1)
            fn_part, ext = split_fn[0], split_fn[1]
            train_part = 'train' if not SystemConfig.skip_validation else 'train_all'
            self.filenames = {True: f'{fn_part}_{train_part}.{ext}', False: f'{fn_part}_valid.{ext}'}
        else:
            self.filenames = {None: filename}
        self.meta_filename = os.path.join(self.base_path, meta_filename) if meta_filename else None
        self.mode = mode

    def load(self, is_train: Optional[bool]) -> Tuple[pd.DataFrame, dict]:
        filename = self.filenames[is_train]
        assert os.path.exists(filename), f"Loader couldn't find file {filename}"
        if self.mode == 'pkl':
            with open(filename, 'rb') as file:
                inp = pkl.load(file)
            if type(inp) is tuple:
                dataset, meta = inp
            else:
                dataset = inp
                meta = {}
        elif self.mode == 'hdf':
            dataset = pd.read_hdf(filename)
            with pd.HDFStore(filename) as store:
                attrs = store.get_storer(self.key).attrs
                meta = attrs.meta if hasattr(attrs, 'meta') else {}
        else:
            raise AssertionError(f'Internal Loader error: no load mode {self.mode}')
        if self.meta_filename:
            with open(self.meta_filename, 'rb') as file:
                meta = pkl.load(file)
        if isinstance(dataset, list):
            dataset = pd.DataFrame(dataset)
        return dataset, meta

    def prepare(self, dataset=None, meta=None):
        if dataset is not None:
            raise ValueError(
                f'Loader should be at the begging of the preparators pipeline, instead received {type(dataset)}')
        return self.load(is_train=meta.get('is_train'))
