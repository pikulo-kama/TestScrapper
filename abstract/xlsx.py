from abc import ABC, abstractmethod
from typing import AnyStr, List, Any


class XLSXExporter(ABC):

    @abstractmethod
    def export(self):
        pass

    @abstractmethod
    def addRow(self, row: List[AnyStr]):
        pass

    @abstractmethod
    def addRows(self, rows: List[Any]):
        pass
