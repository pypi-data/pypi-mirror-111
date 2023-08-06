from . import BasePreparator


class Remover(BasePreparator):
    def __init__(self, columns):
        self.drop_columns = [columns] if isinstance(columns, str) else columns

    def prepare(self, dataset, meta):
        drop_columns = [c for c in self.drop_columns if c in dataset.columns]
        dataset = dataset.drop(columns=drop_columns)
        return dataset, meta
