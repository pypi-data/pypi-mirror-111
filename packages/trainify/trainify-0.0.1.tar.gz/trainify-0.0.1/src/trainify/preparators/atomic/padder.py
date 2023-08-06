import logging
from tqdm import tqdm
import numpy as np

from . import BasePreparator


class Padder(BasePreparator):
    def __init__(self, max_len=None):
        self.max_len = max_len

    def pad_input(self, inp, pad_value, pad_len, bar=None):
        assert len(inp) <= pad_len
        shape = (pad_len,) + (inp.shape[1:] if hasattr(inp, 'shape') else ())
        res = np.ones(shape=shape, dtype=np.long) * pad_value
        res[:len(inp)] = inp
        if bar is not None:
            bar.update()
        return res

    def prepare(self, dataset, meta):
        pad_map = meta['pad_map']
        logging.info('Started padding')
        original_len = len(dataset)
        sequential_input = next(iter(pad_map.keys()))
        if self.max_len is None:
            self.max_len = dataset.loc[:, sequential_input].apply(len).max()
            logging.info(f'Padding length assigned to {self.max_len}')
        else:
            dataset = dataset.loc[dataset.loc[:, sequential_input].apply(
                lambda x: len(x) <= self.max_len)].reset_index(drop=True)
            logging.info(f'Using {len(dataset)} of {original_len} total samples')
        for input_name, pad_value in pad_map.items():
            if np.isnan(pad_value):
                continue
            with tqdm(total=len(dataset), desc=f'Padding {input_name}') as bar:
                dataset.loc[:, input_name] = dataset.loc[:, input_name].apply(
                    lambda x: self.pad_input(x, pad_value, self.max_len, bar))
        return dataset, meta
