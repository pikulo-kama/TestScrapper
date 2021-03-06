from abc import ABC, abstractmethod
from typing import List

from models import DataEntry


class DataEntryMapper(ABC):

    @abstractmethod
    def map(self, record: str) -> List[DataEntry]:
        pass


class PDFFormatter(ABC):

    @abstractmethod
    def formatPage(self, page: object) -> str:
        pass


class PDFParser(ABC):

    @abstractmethod
    def parseDocument(self, documentPath: str) -> bool:
        pass

    @abstractmethod
    def getPageFormatted(self, pageNumber: int) -> str:
        pass

    @abstractmethod
    def getAllPagesFormatted(self, offset: int = 0, limit: int = None) -> List[str]:
        pass
