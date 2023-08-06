from . import BasePreparator


class Adder(BasePreparator):
    def __init__(self, label, value):
        self.label = label
        self.value = value

    def prepare(self, dataset, meta):
        dataset[self.label] = self.value
        return dataset, meta
