from . import BasePreparator


class Dropper(BasePreparator):
    def __init__(self, n: int = None, frac: float = None, replace: bool = False):
        self.frac = frac
        self.n = n
        assert self.frac is None or self.n is None
        assert self.frac is not None or self.n is not None
        self.replace = replace

    def prepare(self, dataset, meta):
        return dataset.sample(frac=self.frac, n=self.n, replace=self.replace).reset_index(drop=True), meta


class Shuffler(Dropper):
    def __init__(self):
        super().__init__(frac=1, replace=False)
