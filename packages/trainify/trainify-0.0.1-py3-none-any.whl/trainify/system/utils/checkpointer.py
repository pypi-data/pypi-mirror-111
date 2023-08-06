import os

import torch
from torch.optim.optimizer import Optimizer

from trainify.configs import SystemConfig


class Checkpointer:
    def __init__(self, path):
        if not os.path.exists(path):
            raise ValueError(f'Checkpointer root path {path} does not exist')
        self.root = path
        self.active = True

    def epoch_step_path(self, epoch, step=None):
        return os.path.join(self.root, f'epoch_{epoch}{(f"_{step}" if step else "")}')

    def model_checkpoint_fn(self, epoch, step=None):
        return os.path.join(self.epoch_step_path(epoch, step), 'model.pt')

    def optimizer_checkpoint_fn(self, epoch, step=None):
        return os.path.join(self.epoch_step_path(epoch, step), 'optimizer.pt')

    def amp_checkpoint_fn(self, epoch, step=None):
        return os.path.join(self.epoch_step_path(epoch, step), 'amp.pt')

    def save(self, model: torch.nn.Module, optimizer: Optimizer, epoch: int, step: int = None):
        if not self.active:
            return
        os.makedirs(self.epoch_step_path(epoch, step))
        torch.save(
            {k.replace('module.', ''): v for k, v in model.state_dict().items()}, self.model_checkpoint_fn(epoch, step))
        torch.save(optimizer.state_dict(), self.optimizer_checkpoint_fn(epoch, step))
        if SystemConfig.use_amp and not SystemConfig.distributed:
            import apex
            torch.save(apex.amp.state_dict(), self.amp_checkpoint_fn(epoch, step))

        # duplicated save for out-of-the-box use for huggingface transformer models
        if hasattr(model, 'save_pretrained'):
            model_path = os.path.join(self.epoch_step_path(epoch, step), 'model')
            os.makedirs(model_path)
            model.save_pretrained(model_path)

    def load(self, epoch, step=None):
        model_state_dict = torch.load(self.model_checkpoint_fn(epoch, step), map_location='cpu')
        optimizer_state_dict = torch.load(self.optimizer_checkpoint_fn(epoch, step), map_location='cpu')
        if SystemConfig.use_amp and not SystemConfig.distributed:
            import apex
            apex.amp.load_state_dict(torch.load(self.amp_checkpoint_fn(epoch, step), map_location='cpu'))
        return model_state_dict, optimizer_state_dict
