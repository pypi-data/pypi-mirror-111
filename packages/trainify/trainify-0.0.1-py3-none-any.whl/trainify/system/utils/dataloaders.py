from typing import Dict, List
import logging
import operator
from collections import defaultdict
from math import ceil
import torch

from .samplers import BaseSampler

from trainify.configs import SystemConfig


class SingleTaskLoader:
    def __init__(self, sampler: BaseSampler):
        self.sampler = sampler
        self.accumulation_size = SystemConfig.total_size // SystemConfig.batch_size
        self.cur_ind = 0

    def reset(self):
        self.sampler.reset()
        self.cur_ind = 0

    def set_rank(self, rank: int):
        self.sampler.set_rank(rank)

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.sampler)

    def __next__(self):
        batch = self.sampler.sample(SystemConfig.batch_size)
        accumulate = self.accumulation_size if self.cur_ind > 0 else 0
        self.cur_ind = (self.cur_ind + 1) % self.accumulation_size
        return batch, accumulate


class MultiDataLoader:
    def __init__(self, samplers: Dict[str, BaseSampler]):
        self.samplers = samplers

        self.common_inputs = [
            inp for inp in next(iter(self.samplers.values())).get_input_names()
            if all(mult_inp != inp and mult_inp not in inp.split('/') for mult_inp in SystemConfig.multitask_inputs)]

        for inp in self.common_inputs:
            for task, sampler in samplers.items():
                if inp not in sampler.get_input_names():
                    raise ValueError(
                        f'input {inp} not included in Config.multitask_inputs but not present for task {task}')

        self.task_inputs = {task: [inp for inp in sampler.get_input_names() if inp not in self.common_inputs]
                            for task, sampler in self.samplers.items()}

        self.tasks = list(self.samplers.keys())
        self.tasks_amount = len(self.samplers)

        self.loader_lengths = {task: sampler.__len__() for task, sampler in self.samplers.items()}
        self.remaining_lengths = self.loader_lengths.copy()

        self.batch_size = SystemConfig.batch_size
        self.total_size = SystemConfig.total_size
        if self.total_size % self.batch_size:
            raise ValueError('total_size should be either None or proportional to batch_size')

        if SystemConfig.distributed:
            self.rank = None
            self.world_size = SystemConfig.world_size
            self.step = 0

        self.cur_size = self.total_size
        self.active = {task: True for task in self.tasks}

        self.remaining_samples = {}
        self.delayed_activations = []
        self.delayed_deactivations = []
        self.size_changed = False

    @property
    def active_tasks(self) -> List[str]:
        return [task for task in self.tasks if self.active[task]]

    @property
    def accumulate(self) -> bool:
        return self.remaining_samples and sum(self.remaining_samples.values()) > 0

    def activate_task(self, task: str):
        if not self.accumulate:
            self.active[task] = True
        else:
            self.delayed_activations.append(task)

    def deactivate_task(self, task: str):
        if not self.accumulate:
            self.active[task] = False
        else:
            self.delayed_deactivations.append(task)

    def activate_all_tasks(self):
        if not self.accumulate:
            self.active = {task: True for task in self.tasks}
        else:
            self.delayed_activations = self.tasks

    def deactivate_all_tasks(self):
        if not self.accumulate:
            self.active = {task: False for task in self.tasks}
        else:
            self.delayed_deactivations = self.tasks

    def set_rank(self, rank: int):
        self.rank = rank

    def _split_batch_by_tasks(self):
        if not self.accumulate \
                and (sum([self.remaining_lengths[task] for task in self.active_tasks]) < self.total_size
                     or any(self.remaining_lengths[task] < 1 for task in self.active_tasks)):
            self.finish()
        total_length = sum([self.remaining_lengths[task] for task in self.active_tasks])
        task_proportions = {task: self.remaining_lengths[task] / total_length for task in self.active_tasks}
        task_sizes = {task: int(round(self.cur_size * task_proportion))
                      for task, task_proportion in task_proportions.items()}
        while sum(task_sizes.values()) > self.cur_size:
            task_sizes[max(task_sizes.items(), key=operator.itemgetter(1))[0]] -= 1
        while sum(task_sizes.values()) < self.cur_size:
            task_sizes[max(task_sizes.items(), key=operator.itemgetter(1))[0]] += 1
        for task in self.active_tasks:
            if task_sizes[task] < 1:
                self.cur_size = ((ceil(1 / min(task_proportions.values())) - 1) // self.batch_size + 1) \
                                * self.batch_size
                if not self.size_changed:
                    logging.info('Size changed to ', self.cur_size)
                    self.size_changed = True
                if self.cur_size > sum(self.remaining_lengths[task] for task in self.active_tasks):
                    self.finish()
                return self._split_batch_by_tasks()
        return task_sizes

    def _next_batch_by_task(self, task: str, size: int):
        assert self.remaining_lengths[task] >= size
        self.remaining_lengths[task] -= size
        return self.samplers[task].sample(batch_size=size)

    def _subsample_batch(self):
        new_sizes = {}
        samples_left = self.batch_size
        for task in self.active_tasks:
            if self.remaining_samples[task] == 0:
                continue
            if self.remaining_samples[task] > samples_left:
                new_sizes[task] = samples_left
                self.remaining_samples[task] -= samples_left
                break
            else:
                new_sizes[task] = self.remaining_samples[task]
                self.remaining_samples[task] = 0
                samples_left -= new_sizes[task]
        assert sum(new_sizes.values()) == self.batch_size
        return new_sizes

    def _get_task_sizes(self) -> Dict[str, int]:
        if not self.accumulate:
            for task in self.delayed_activations:
                self.activate_task(task)
            self.delayed_activations = []
            for task in self.delayed_deactivations:
                self.deactivate_task(task)
            self.delayed_deactivations = []

        if self.accumulate:
            return self._subsample_batch()
        self.cur_size = self.total_size
        task_sizes = self._split_batch_by_tasks()
        if self.cur_size != self.batch_size:
            self.remaining_samples = task_sizes.copy()
            task_sizes = self._subsample_batch()
        return task_sizes

    def _get_batch(self, task_sizes):
        if not SystemConfig.distributed:
            return {task: self._next_batch_by_task(task, size) for task, size in task_sizes.items()}, task_sizes

        if self.rank is None:
            raise ValueError('Rank not set in dataloader')

        worker_ind = self.rank  # (self.rank + self.step) % self.world_size
        self.step += 1
        worker_range = (
            self.batch_size // self.world_size * worker_ind,
            self.batch_size // self.world_size * (worker_ind + 1))
        total_ind = 0
        batch = {}
        worker_task_sizes = {}
        for task, size in task_sizes.items():
            task_batch = self._next_batch_by_task(task, size)
            if total_ind + size < worker_range[0] or total_ind >= worker_range[1]:
                total_ind += size
                continue
            task_range = range(max(worker_range[0] - total_ind, 0), min(worker_range[1] - total_ind, size))
            if len(task_range) == 0:
                total_ind += size
                continue
            worker_task_sizes[task] = len(task_range)
            batch[task] = {
                key: ({k: v[task_range] for k, v in value.items()} if type(value) is dict else value[task_range])
                for key, value in task_batch.items()}
            total_ind += size
        return batch, worker_task_sizes

    def reset(self):
        for sampler in self.samplers.values():
            sampler.reset()
        self.remaining_lengths = self.loader_lengths.copy()
        self.remaining_samples = None
        self.cur_size = self.total_size

    def finish(self):
        self.reset()
        raise StopIteration

    def __iter__(self):
        return self

    def __len__(self):
        return sum([self.loader_lengths[task] for task in self.active_tasks]) // self.batch_size

    @classmethod
    def get_nested_dict(cls, inp_dict: dict) -> dict:
        nested_dict = defaultdict(dict)
        for key, value in inp_dict.items():
            if '/' in key:
                outer_key, inner_key = key.split(sep='/', maxsplit=1)
                nested_dict[outer_key].update(cls.get_nested_dict({inner_key: value}))
            else:
                nested_dict[key] = value
        return dict(nested_dict)

    def __next__(self):
        if not self.active_tasks:
            raise ValueError('No tasks activated')

        task_sizes = self._get_task_sizes()
        batch, task_sizes = self._get_batch(task_sizes)

        task_ids = {}
        cur_ind = 0
        for task, size in task_sizes.items():
            task_ids[task] = list(range(cur_ind, cur_ind + size))
            cur_ind += size

        new_batch = defaultdict(dict, {
            inp: torch.cat([batch[task][inp]
                            for task in batch.keys()], dim=0) if len(batch) > 1 else next(iter(batch.values()))[inp]
            for inp in self.common_inputs})

        for task, inputs in self.task_inputs.items():
            if task in batch.keys():
                for inp in inputs:
                    new_batch[inp][task] = batch[task][inp]

        batch = self.get_nested_dict(new_batch)

        return task_ids, batch, self.cur_size // self.batch_size if self.accumulate else 0

    def share_memory_(self):
        for sampler in self.samplers.values():
            if hasattr(sampler, 'share_memory_'):
                sampler.share_memory_()


class DatasetCoeffsLoader(MultiDataLoader):
    def __init__(self, samplers: dict):
        super().__init__(samplers)
        self.dataset_coeffs = SystemConfig.dataset_coeffs
        for task, coeff in self.dataset_coeffs.items():
            self.loader_lengths[task] = int(round(self.loader_lengths[task] * coeff))
        self.remaining_lengths = self.loader_lengths.copy()

    def _next_batch_by_task(self, task, size):
        assert self.remaining_lengths[task] >= size
        self.remaining_lengths[task] -= size
        try:
            return self.samplers[task].sample(batch_size=size)
        except StopIteration:
            return self.samplers[task].sample(batch_size=size)

    def reset(self):
        self.remaining_lengths = self.loader_lengths.copy()
        self.remaining_samples = None
        self.cur_size = self.total_size
