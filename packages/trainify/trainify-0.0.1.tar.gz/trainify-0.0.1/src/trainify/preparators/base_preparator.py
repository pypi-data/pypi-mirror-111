from abc import ABC, abstractmethod
from typing import Optional, Tuple, List, Union
import pandas as pd


class BasePreparator(ABC):
    @abstractmethod
    def prepare(self, dataset: Optional[pd.DataFrame], meta: Optional[dict]) -> Tuple[pd.DataFrame, dict]:
        pass


Preparators = Union[BasePreparator, List['Preparators'], Tuple['Preparators', ...]]
