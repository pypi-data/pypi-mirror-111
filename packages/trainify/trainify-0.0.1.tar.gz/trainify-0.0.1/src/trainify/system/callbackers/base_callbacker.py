from typing import Optional, Set, DefaultDict
from abc import ABC, abstractmethod
from collections import defaultdict

from ..utils.averagers import Averager, MeanAverager


class BaseCallbacker(ABC):
    def __init__(self, averager_cls: Optional[type(Averager)] = None):
        self.val_mode = False
        self.callbacks: DefaultDict[str, Averager] = defaultdict(MeanAverager if averager_cls is None else averager_cls)
        self.active_callbacks: Set[str] = set()

    def train(self):
        if self.val_mode:
            self.val_mode = False
            self.reset()

    def eval(self):
        if not self.val_mode:
            self.val_mode = True
            self.reset()

    def get_values(self) -> dict:
        return {key: self.callbacks[key].get() for key in self.active_callbacks}

    @abstractmethod
    def update(self, **kwargs):
        pass

    def update_values(self, update_dict: dict):
        for key, value in update_dict.items():
            self.callbacks[key].upd(value)
            self.active_callbacks.add(key)

    def write(self, tb_writer, step):
        for name, value in self.get_values().items():
            if tb_writer is not None:
                tb_writer.add_scalar(name, value, step)

    def reset(self):
        self.active_callbacks = set()
        for callback in self.callbacks.values():
            callback.reset()
