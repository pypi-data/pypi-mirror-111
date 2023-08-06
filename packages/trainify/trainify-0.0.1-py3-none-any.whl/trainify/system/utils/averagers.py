from abc import ABC, abstractmethod
import operator
from collections import defaultdict
import torch

from trainify.configs import SystemConfig


class Averager(ABC):
    def __init__(self, initial_value=0, reduce=True):
        self.initial_value = initial_value
        self.reduce = reduce

    @abstractmethod
    def upd(self, val):
        pass

    @abstractmethod
    def calculate(self):
        pass

    def get(self):
        value = self.calculate()
        if self.reduce and SystemConfig.distributed and isinstance(value, torch.Tensor):
            import torch.distributed as dist
            dist.reduce(tensor=value, dst=0, op=dist.ReduceOp.SUM)
            value /= SystemConfig.world_size
        return value

    @abstractmethod
    def reset(self):
        pass

    def __str__(self):
        return self.get()


class MeanAverager(Averager):
    def __init__(self, initial_value=0.):
        super().__init__(initial_value)
        self.sum = self.initial_value
        self.cnt = 1 if self.initial_value else 0

    def upd(self, val):
        self.sum += val
        self.cnt += 1

    def calculate(self):
        return self.sum / self.cnt if self.cnt != 0 else 0

    def reset(self):
        self.sum = self.initial_value
        self.cnt = 1 if self.initial_value else 0


class MostOftenAverager(Averager):
    def __init__(self, initial_value=0.):
        super().__init__(initial_value, reduce=False)
        self.value_counts = defaultdict(int)

    def upd(self, val):
        self.value_counts[val.item() if isinstance(val, torch.Tensor) else val] += 1

    def calculate(self):
        return max(
            self.value_counts.items(), key=operator.itemgetter(1))[0] if self.value_counts else self.initial_value

    def reset(self):
        self.value_counts = defaultdict(int)


class ExpAverager(Averager):
    """
    Exponential moving average
    """

    def __init__(self, alpha, initial_value=0):
        super().__init__(initial_value)
        self.sum = self.initial_value
        self.alpha = alpha

    def upd(self, val):
        self.sum = self.alpha * self.sum + (1 - self.alpha) * val

    def calculate(self):
        return self.sum

    def reset(self):
        self.sum = self.initial_value
