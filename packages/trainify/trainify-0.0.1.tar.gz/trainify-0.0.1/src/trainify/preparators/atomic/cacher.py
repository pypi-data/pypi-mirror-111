from typing import Optional, Tuple
import os
import pickle as pkl
import pandas as pd

from .loader import Loader

from trainify.configs import SystemConfig


class Cacher(Loader):
    base_path = SystemConfig.data_path
    key = SystemConfig.hdf_key

    def __init__(self, filename: str, rewrite: bool = False, mode: Optional[str] = None):
        super().__init__(filename=filename, meta_filename=None, mode=mode)
        self.rewrite = rewrite
        self.pickle_protocol: int = SystemConfig.pickle_protocol

    def ready(self) -> bool:
        return all(os.path.exists(filename) for filename in self.filenames.values()) and not self.rewrite

    @staticmethod
    def create_directory_if_needed(path: str):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

    def prepare(self, dataset=None, meta=None) -> Tuple[pd.DataFrame, dict]:
        if self.ready():
            return self.load(is_train=meta.get('is_train'))
        assert dataset is not None and meta is not None, \
            "Cacher received None inputs, but couldn't load previously saved data"
        filename = self.filenames[meta.get('is_train')]
        self.create_directory_if_needed(filename)
        if self.mode == 'pkl':
            with open(filename, 'wb') as file:
                pkl.dump((dataset, meta), file, protocol=self.pickle_protocol)
        elif self.mode == 'hdf':
            dataset.to_hdf(filename, key=self.key)
            with pd.HDFStore(filename) as store:
                store.get_storer(self.key).attrs.meta = meta

        return dataset, meta
