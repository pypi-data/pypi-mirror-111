from typing import Optional, List
import torch

from . import ConfigMetaClass, SystemConfig

from trainify.system.utils.dataloaders import SingleTaskLoader
from trainify.system.trainers.trainer import Trainer
from trainify.system.callbackers import (BaseCallbacker, LossCallbacker, AccuracyCallbacker,
                                                   AuxillaryCallbacker, ModelCallbacker)

from trainify.preparators import Preparators, Cacher


def recursive_cacher_check(preparators: Preparators, paths: Optional[set] = None):
    if paths is None:
        paths = set()
    if isinstance(preparators, list) or isinstance(preparators, tuple):
        for sub_prep in preparators:
            recursive_cacher_check(sub_prep, paths)
    elif isinstance(preparators, dict):
        for sub_prep in preparators.values():
            recursive_cacher_check(sub_prep, paths)
    elif isinstance(preparators, Cacher):
        for filename in preparators.filenames.values():
            if filename in paths:
                raise ValueError(f'Multiple Cachers use same filename: {filename}')
            paths.add(filename)


class Components(metaclass=ConfigMetaClass):
    model: Optional[torch.nn.Module] = None
    optimizer = torch.optim.Adam
    scheduler = None
    preparators = None
    dataloader = SingleTaskLoader
    trainer: type(Trainer) = Trainer
    callbackers: List[BaseCallbacker] = [
        LossCallbacker(), AccuracyCallbacker(), AuxillaryCallbacker(), ModelCallbacker()]

    @classmethod
    def init(cls):
        if SystemConfig.distributed:
            from trainify.system.trainers import ParallelTrainerWrapper
            cls.trainer = ParallelTrainerWrapper(cls.trainer)

        if len(SystemConfig.tasks) == 1 and not isinstance(cls.preparators, dict):
            cls.preparators = {SystemConfig.tasks[0]: cls.preparators}

        recursive_cacher_check(cls.preparators)
