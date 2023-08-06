import logging
from tqdm import tqdm
import torch

from .base_trainer import BaseTrainer
from trainify.configs import SystemConfig


class Trainer(BaseTrainer):
    def train_step(self, batch, accumulate, accumulation_size):
        if SystemConfig.val_log_freq and self.absolute_step % SystemConfig.val_log_freq == 0:
            if self.absolute_step != 0 or SystemConfig.validate_at_start:
                self._write_val_logs()

        outputs = self.model(**batch, accumulate=accumulate)

        loss = outputs['loss']
        if torch.isnan(loss).any():
            raise ValueError('Loss is nan')
        outputs['loss'] = loss.detach()
        if accumulate:
            loss /= accumulate
        elif accumulation_size:
            loss /= accumulation_size

        if SystemConfig.use_amp:
            import apex
            with apex.amp.scale_loss(loss, self.optimizer) as scaled_loss:
                scaled_loss.backward()
        else:
            loss.backward()
        del loss

        if not accumulate:
            self.optimizer.step()
            if self.scheduler is not None:
                self.scheduler.step()
            self.optimizer.zero_grad()

        if SystemConfig.train_metrics_freq and self.absolute_step % SystemConfig.train_metrics_freq == 0:
            self.callbackers.update(training_mode=True, outputs=outputs, epoch=self.epoch, lr=self.lr)

        if (SystemConfig.checkpoint_step_freq and (self.absolute_step % SystemConfig.checkpoint_step_freq == 0)
                and self.absolute_step != 0):
            self.checkpointer.save(self.model, self.optimizer, self.epoch, self.absolute_step)

        if SystemConfig.train_log_freq and self.absolute_step % SystemConfig.train_log_freq == 0:
            self._write_train_logs()

        self.absolute_step += 1

    def train_core(self):
        if self.enable_logging:
            logging.info('Training started')
        self.model.train()
        if self.start_step is not None:
            assert self.start_step >= 0, \
                'Wrong restoration step, checkpoint was probably trained with different configs'
        else:
            self.start_step = -1
        accumulation_size = None
        for self.epoch in range(self.epoch, SystemConfig.epochs + 1):
            for batch, accumulate in tqdm(
                    self.train_dataloader, desc=f'Training epoch {self.epoch}', disable=not self.enable_logging):
                if self.absolute_step <= self.start_step:
                    self.absolute_step += 1
                    continue
                self.train_step(batch, accumulate, accumulation_size)
                accumulation_size = accumulate

            if hasattr(self.model, 'reset'):
                self.model.reset()

            if SystemConfig.checkpoint_epoch_freq and self.epoch % SystemConfig.checkpoint_epoch_freq == 0:
                self.checkpointer.save(self.model, self.optimizer, self.epoch)

    def train(self):
        try:
            self.train_core()
        except Exception as e:
            if not isinstance(e, KeyboardInterrupt) and self.absolute_step > 2:
                self.checkpointer.save(self.model, self.optimizer, self.epoch, self.absolute_step)
            raise
