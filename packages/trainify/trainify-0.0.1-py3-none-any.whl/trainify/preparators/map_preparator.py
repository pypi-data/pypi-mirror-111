from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple, Dict
import tqdm
import pandas as pd

from . import BasePreparator


class MapPreparator(BasePreparator, ABC):
    def __init__(self, desc: Optional[str], delete_old: bool = True):
        self.desc = desc
        self.delete_old = delete_old

    @abstractmethod
    def process_row(self, **kwargs) -> Dict[str, Any]:
        pass

    def _process(self, row: pd.Series, bar: tqdm.tqdm) -> Dict[str, Any]:
        result = self.process_row(**row)
        if self.delete_old:
            for key in row.index:
                row[key] = None
        bar.update()
        return result

    def update_meta(self, meta: Dict[str, any]) -> Dict[str, any]:
        return meta

    def prepare(self, dataset: Optional[pd.DataFrame], meta: Optional[dict]) -> Tuple[pd.DataFrame, dict]:
        with tqdm.tqdm(desc=self.desc, total=len(dataset)) as bar:
            return (dataset.apply(lambda row: self._process(row, bar), axis=1, result_type='expand'),
                    self.update_meta(meta))
