from . import BasePreparator


class Filterer(BasePreparator):
    def __init__(self, label, values, remove=False):
        self.label = label
        self.values = values if type(values) is list else [values]
        self.remove = remove

    def prepare(self, dataset, meta):
        filter_lambda = (lambda x: x not in self.values) if self.remove else (lambda x: x in self.values)
        return dataset[dataset.loc[:, self.label].apply(filter_lambda)].reset_index(drop=True), meta
