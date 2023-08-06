from typing import Type
import logging
import os
import pickle as pkl
import torch
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.multiprocessing as mp

from .base_trainer import BaseTrainer

import trainify.configs as configs
from trainify.configs import SystemConfig

exp_environ_key = 'EXP_NAME'


def train_func(rank, trainer):
    logging.info(f'Spawned process with rank {rank}')
    trainer.train_distr(rank)


def ParallelTrainerWrapper(trainer_cls: Type[BaseTrainer]) -> Type[BaseTrainer]:
    def __init__(self, model, optimizer, scheduler, dataloaders, callbackers, checkpointer, start_epoch, start_step):
        trainer_cls.__init__(
            self, model, None, scheduler, dataloaders, callbackers, checkpointer, start_epoch, start_step)

        self.num_gpus = SystemConfig.num_gpus
        self.gpus_per_model = SystemConfig.gpus_per_model

        # optimizer pickled to avoid error caught in mp.spawn after restoring optimizer.state_dict
        # in torch/multiprocessing/reductions.py reduce_storage, line 333
        # RuntimeError: unable to open shared memory object in read-write mode
        # probably because there isn't enough shared memory
        self.optimizer_cls = type(optimizer)
        self.scheduler_cls = type(scheduler) if scheduler is not None else None
        os.makedirs('tmp', exist_ok=True)
        torch.save(optimizer.state_dict(), 'tmp/optimizer.pkl')

    class DDPX(DDP):
        def _ddp_init_helper(self):
            for attr in ('save_pretrained', 'reset'):
                if hasattr(self.module, attr):
                    setattr(self, attr, getattr(self.module, attr))
            self.device_ids = None
            super()._ddp_init_helper()

        def forward(self, *inputs, accumulate=False, **kwargs):
            return self.module(*inputs, **kwargs) if accumulate or not self.module.training \
                else super().forward(*inputs, **kwargs)

    if SystemConfig.distributed_type == 'apex':
        from apex.parallel import DistributedDataParallel as ApexDDP

        class ApexDDPX(ApexDDP):
            def __init__(self, *inputs, **kwargs):
                super().__init__(*inputs, **kwargs)
                for attr in ('save_pretrained', 'reset'):
                    if hasattr(self.module, attr):
                        setattr(self, attr, getattr(self.module, attr))

            def forward(self, *inputs, accumulate=False, **kwargs):
                outputs = super().forward(*inputs, **kwargs)
                if not self.module.training:
                    loss = outputs['loss'].detach()
                    dist.reduce(tensor=loss, dst=0, op=dist.ReduceOp.SUM)
                    outputs['loss'] = loss
                return outputs

    def train_distr(self, rank):
        logging.info(f'Initializing process with rank {rank}')

        local_rank = rank
        if SystemConfig.node_rank is not None:
            SystemConfig.num_nodes = int(SystemConfig.num_nodes)
            SystemConfig.node_rank = int(SystemConfig.node_rank)
            rank += SystemConfig.num_gpus * SystemConfig.node_rank

        dist.init_process_group(
            backend='nccl', init_method=SystemConfig.init_method, rank=rank, world_size=SystemConfig.world_size)

        self.devices = [SystemConfig.parallel_devices[self.gpus_per_model * local_rank + ind]
                        for ind in range(self.gpus_per_model)]
        self.device = self.devices[0]
        SystemConfig.devices = self.devices
        SystemConfig.device = self.device

        if hasattr(self.model, 'to_devices_'):
            self.model.to_devices_(self.devices)
        elif SystemConfig.gpus_per_model == 1:
            self.model = self.model.to(self.devices[0])
        else:
            raise ValueError('multi-gpu models should have to_devices_(devices) method defined')

        self.optimizer = self.optimizer_cls(
            self.model.optimizer_parameters() if hasattr(self.model, 'optimizer_parameters')
            else self.model.parameters(), lr=SystemConfig.lr, **SystemConfig.optimizer_kwargs)

        self.scheduler = self.scheduler_cls(self.optimizer) if self.scheduler_cls is not None else None

        torch.cuda.set_device(self.devices[0])

        if SystemConfig.use_amp:
            import apex
            self.model = apex.parallel.convert_syncbn_model(self.model)
            self.model, self.optimizer = apex.amp.initialize(
                self.model, self.optimizer,
                opt_level=SystemConfig.amp_opt_level, max_loss_scale=SystemConfig.amp_max_loss_scale, min_loss_scale=1)
            with open('tmp/optimizer.pkl', 'rb') as file:
                self.optimizer.load_state_dict(pkl.load(file))
        else:
            self.optimizer.load_state_dict(torch.load('tmp/optimizer.pkl', map_location='cpu'))

        if SystemConfig.distributed_type == 'apex':
            self.model = ApexDDPX(self.model, gradient_predivide_factor=SystemConfig.num_gpus * SystemConfig.batch_size)
        else:
            self.model = DDPX(self.model, find_unused_parameters=SystemConfig.find_unused_parameters)

        self.model.train()

        if self.train_dataloader is not None:
            self.train_dataloader.set_rank(rank)
        if self.val_dataloaders is not None:
            for val_dataloader in self.val_dataloaders.values():
                val_dataloader.set_rank(rank)
        if rank != 0:
            self.callbackers.active = False
            self.checkpointer.active = False
            self.enable_logging = False
        else:
            os.remove('tmp/optimizer.pkl')

        trainer_cls.train(self)

    def train(self):
        os.environ[exp_environ_key] = SystemConfig.exp
        os.environ['MASTER_ADDR'] = SystemConfig.master_addr
        os.environ['MASTER_PORT'] = str(SystemConfig.master_port)
        logging.info('Spawning train processes')
        mp.spawn(train_func, args=(self,), nprocs=self.num_gpus // self.gpus_per_model, join=True)

    global ParallelTrainer
    ParallelTrainer = type(
        'ParallelTrainer',
        (trainer_cls,),
        {'__init__': __init__, 'train': train, 'train_distr': train_distr})

    return ParallelTrainer


exp = os.environ.get(exp_environ_key)
if exp is not None and SystemConfig.exp is None:
    configs.init(exp)
