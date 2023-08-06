from typing import List
from torch.utils.tensorboard import SummaryWriter

from trainify.system.callbackers import BaseCallbacker


class CallbackerModule:
    def __init__(self, callbackers: List[BaseCallbacker], logs_path: str):
        self.callbackers = callbackers
        self.logs_path = logs_path
        self.tb_writer = None
        self.active = True

    def update(self, training_mode: bool = True, **kwargs):
        for callbacker in self.callbackers:
            if training_mode:
                callbacker.train()
            else:
                callbacker.eval()
            callbacker.update(**kwargs)

    def write(self, absolute_step: int):
        if self.tb_writer is None and self.active:
            self.tb_writer = SummaryWriter(log_dir=self.logs_path)
        for callbacker in self.callbackers:
            callbacker.write(self.tb_writer, absolute_step)
            callbacker.reset()
