from abc import abstractmethod
from typing import Tuple, Dict, Optional
from tqdm import tqdm

import torch

from trainify.system.utils.callbacker_module import CallbackerModule
from trainify.configs import SystemConfig

from ..utils.dataloaders import MultiDataLoader
from ..utils.checkpointer import Checkpointer


class BaseTrainer:
    def __init__(
            self, model: torch.nn.Module, optimizer, scheduler,
            dataloaders: Tuple[MultiDataLoader, Dict[str, MultiDataLoader]],
            callbackers: CallbackerModule, checkpointer: Checkpointer, start_epoch: int, start_step: Optional[int]):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.train_dataloader, self.val_dataloaders = dataloaders
        self.callbackers = callbackers
        self.checkpointer = checkpointer
        self.start_epoch = start_epoch
        self.start_step = start_step

        self.tasks = SystemConfig.tasks
        self.n_tasks = len(self.tasks)
        self.absolute_step = 0
        self.epoch = self.start_epoch
        self.device = SystemConfig.device
        self.enable_logging = True

    @property
    def lr(self):
        return self.optimizer.param_groups[0]['lr']

    def _write_train_logs(self):
        self.callbackers.write(self.absolute_step)

    def _write_val_logs(self):
        self.model.eval()

        for task, val_dataloader in self.val_dataloaders.items():
            for batch, _ in tqdm(
                    val_dataloader, desc=f'Validation at step {self.absolute_step}', disable=not self.enable_logging):
                with torch.no_grad():
                    outputs = self.model(**batch)
                    self.callbackers.update(training_mode=False, outputs=outputs, epoch=self.epoch, lr=self.lr)
            self.callbackers.write(self.absolute_step)

        self.model.train()

    @abstractmethod
    def train(self):
        pass
