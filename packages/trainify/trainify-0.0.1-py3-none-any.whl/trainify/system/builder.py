from typing import Optional
import logging
import os
import time

from trainify.configs import SystemConfig, Components
from .utils.builder_utils import init_logging, create_checkpointer, prepare_data, create_model, create_optimizer
from .utils.checkpointer import Checkpointer
from trainify.system.utils.callbacker_module import CallbackerModule


class Builder:
    def __init__(self):
        self.base_logs_path = os.path.join(
            SystemConfig.logs_path, SystemConfig.logs_name if SystemConfig.logs_name else SystemConfig.exp_path)

        self.logs_path = os.path.join(
            self.base_logs_path, time.strftime(SystemConfig.date_format), time.strftime(SystemConfig.time_format))

        init_logging(self.logs_path)

        self.checkpointer = create_checkpointer(self.logs_path)
        self.callbackers = CallbackerModule(Components.callbackers, self.logs_path)

        self.dataloaders = prepare_data()

        self.model = create_model()
        self.optimizer = create_optimizer(self.model)
        self.scheduler = (Components.scheduler(self.optimizer, dataloader_length=len(self.dataloaders[0]))
                          if Components.scheduler is not None else None)

        self.start_epoch = 0
        self.start_step: Optional[int] = None

        if SystemConfig.restore:
            self.restore_checkpoint()

    def restore_checkpoint(self):
        self.start_step = SystemConfig.restore_step
        restorator = Checkpointer(os.path.join(SystemConfig.restore_from, SystemConfig.checkpoints_folder))
        restore_epoch = SystemConfig.restore_epoch if SystemConfig.restore_epoch != 'last' \
            else max([int(file.split('.')[0].split('_')[1]) for file in os.listdir(restorator.root)])
        self.start_epoch = restore_epoch if self.start_step is not None else restore_epoch + 1
        model_state_dict, optimizer_state_dict = restorator.load(restore_epoch, self.start_step)
        self.model.load_state_dict(model_state_dict)
        self.optimizer.load_state_dict(optimizer_state_dict)

        logging.info('Model and optimizer restored')

    def create_trainer(self) -> Components.trainer:
        return Components.trainer(
            model=self.model, optimizer=self.optimizer, scheduler=self.scheduler,
            dataloaders=self.dataloaders, callbackers=self.callbackers, checkpointer=self.checkpointer,
            start_epoch=self.start_epoch, start_step=self.start_step)
