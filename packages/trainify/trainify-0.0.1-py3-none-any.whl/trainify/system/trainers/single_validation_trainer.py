import logging

from .base_trainer import BaseTrainer


class SingleValidationTrainer(BaseTrainer):
    def train(self):
        logging.info('Checkpoint evaluation started')
        self._write_val_logs()
