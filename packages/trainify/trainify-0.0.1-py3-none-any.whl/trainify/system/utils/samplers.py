from typing import Tuple, List, Dict, Optional, Union
from abc import ABC, abstractmethod
from collections import defaultdict
import os
import random
import pandas as pd
import torch

from trainify.configs import SystemConfig


class BaseSampler(ABC):
    @abstractmethod
    def sample(self, batch_size) -> Dict[str, torch.Tensor]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_input_names(self) -> List[str]:
        pass

    @abstractmethod
    def set_rank(self, rank: int):
        pass


class TensorDataset:
    def __init__(self, tensors_dict: Dict[str, torch.Tensor]):
        sizes = [len(value) for value in tensors_dict.values()]
        assert all(size == sizes[0] for size in sizes)
        self.length = sizes[0]
        self.tensors_dict = tensors_dict

    def to(self, device: Union[str, torch.device]):
        self.tensors_dict = {key: value.to(device) for key, value in self.tensors_dict.items()}

    @property
    def inputs_list(self) -> List[str]:
        return list(self.tensors_dict.keys())

    @staticmethod
    def convert_type(x: torch.Tensor) -> torch.Tensor:
        type_map = {
            int_type: torch.long for int_type in (torch.uint8, torch.int8, torch.int16, torch.int32, torch.int64)}
        return x.to(type_map[x.dtype]) if x.dtype in type_map.keys() else x

    def __getitem__(self, index) -> Dict[str, torch.Tensor]:
        return {
            key: self.convert_type(value[index]).to(SystemConfig.device) for key, value in self.tensors_dict.items()}

    def __len__(self) -> int:
        return self.length

    def share_memory_(self):
        for value in self.tensors_dict.values():
            value.share_memory_()


class OMSampler(BaseSampler):
    def __init__(
            self, tensors_dict: Dict[str, torch.Tensor], shuffle: bool = True, device=None, seed: Optional[int] = None):
        self.dataset = TensorDataset(tensors_dict)
        if device is not None:
            self.to(device)
        self.length = len(self.dataset)
        self.shuffle = shuffle
        self.seed = seed
        self.indices = self._create_indices()
        self.position = 0

    def to(self, device: Union[str, torch.device]):
        self.dataset.to(device)

    def reset(self):
        if self.seed is not None:
            self.seed += 1
        self.position = 0
        self.indices = self._create_indices()

    @property
    def get_input_names(self) -> List[str]:
        return self.dataset.inputs_list

    def __len__(self) -> int:
        return self.length

    def _create_indices(self) -> List[int]:
        indices = list(range(self.length))
        if not self.shuffle:
            return indices

        if self.seed is not None:
            random.seed(self.seed)

        random.shuffle(indices)
        return indices

    def sample(self, batch_size: int) -> Dict[str, torch.Tensor]:
        old_position = self.position
        self.position += batch_size
        if self.position > self.length:
            self.reset()
            raise StopIteration
        return self.dataset[self.indices[old_position: self.position]]

    def share_memory_(self):
        self.dataset.share_memory_()


class StorageSampler(BaseSampler):
    sep = SystemConfig.storage_sep
    file_sep = SystemConfig.storage_file_sep
    key = SystemConfig.hdf_key
    ext = SystemConfig.hdf_ext

    def __init__(self, filename: str):
        self.length = None
        self.table_iterator = None
        self.device = None
        self.scalar_inputs = self.vector_inputs = None
        self.dtypes = None
        self.iter = None
        self.filename = filename
        self.rank = None

    def init(self):
        self.filename = f'{self.filename}{self.ext}' if self.rank is None \
            else f'{self.filename}{self.file_sep}{self.rank}{self.ext}'
        assert os.path.exists(self.filename), f'{self.filename} does not exist'
        store = pd.HDFStore(self.filename)
        self.length = store.get_storer(self.key).attrs.len // SystemConfig.batch_size
        self.table_iterator = store.select(self.key, chunksize=SystemConfig.batch_size)
        self.device = SystemConfig.device
        sample = store.select(self.key, start=0, stop=1)
        assert isinstance(sample, pd.DataFrame)
        self.scalar_inputs, self.vector_inputs = self.read_input_names(columns=list(sample.columns), sep=self.sep)
        raw_dtypes = sample.dtypes
        self.dtypes = {}
        for key, dtype in raw_dtypes.items():
            dtype = self.convert_dtype(dtype.name)
            assert isinstance(key, str)
            key = key.split(self.sep)[0]
            if key in self.dtypes:
                assert self.dtypes[key] == dtype
            else:
                self.dtypes[key] = dtype

        assert set(self.get_input_names()) == set(self.dtypes.keys()), 'Internal error: dtypes not read properly'

        self.iter = iter(self.table_iterator)

    @staticmethod
    def convert_dtype(dtype: str):
        if 'bool' in dtype:
            return torch.bool
        elif 'int' in dtype:
            return torch.long
        elif 'float' in dtype:
            return torch.float
        else:
            raise ValueError(f"Dtype {dtype} can't be recognized")

    @staticmethod
    def read_input_names(columns: List[str], sep: str) -> Tuple[List[str], Dict[str, int]]:
        scalar_inputs = []
        vector_inputs = defaultdict(int)
        for key in columns:
            if sep in key:
                core, ind = key.split(sep)
                vector_inputs[core] = max(vector_inputs[core], int(ind))
            else:
                scalar_inputs.append(key)
        vector_inputs = {key: max_ind + 1 for key, max_ind in vector_inputs.items()}
        return scalar_inputs, vector_inputs

    def get_input_names(self) -> List[str]:
        if self.table_iterator is None:
            self.init()
        return self.scalar_inputs + list(self.vector_inputs.keys())

    def set_rank(self, rank: int):
        self.rank = rank

    def sample(self, batch_size: Optional[int] = None) -> Dict[str, torch.Tensor]:
        if self.table_iterator is None:
            self.init()
        try:
            source = next(self.iter).to_dict(orient='list')
        except StopIteration:
            self.reset()
            raise

        inputs = {key: torch.tensor(source[key], device=self.device, dtype=self.dtypes[key]) for key in self.scalar_inputs}

        for key, max_ind in self.vector_inputs.items():
            inputs[key] = torch.stack(
                [torch.tensor(source[f'{key}{self.sep}{ind}'], device=self.device, dtype=self.dtypes[key])
                 for ind in range(max_ind)], dim=-1)
        return inputs

    def reset(self):
        self.iter = iter(self.table_iterator)

    def __len__(self):
        if self.table_iterator is None:
            self.init()
        return self.length

    def to(self, device: Union[str, torch.device]):
        self.device = device
