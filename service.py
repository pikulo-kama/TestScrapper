import re
from typing import List

from abstract.pdf import DataEntryMapper
from models import DataEntry


class DataEntryService:
    _dataEntryMapper: DataEntryMapper

    def __init__(self, dataEntryMapper: DataEntryMapper):
        self._dataEntryMapper = dataEntryMapper

    def splitTextInEntries(self, data: str, splitPattern: str = r'(P\d{3}\s+)') -> List[DataEntry]:
        """
        Function receives whold body of PDF file and then splits it
        by pattern. Then separator is joined with next element.
        So simply function returns data entry in plain format.
        """

        dataEntries = []
        rawDataEntries = re.split(splitPattern, data)

        step = 1

        for idx in range(0, len(rawDataEntries), step):

            if re.fullmatch(splitPattern, rawDataEntries[idx]):
                recordData = f"{rawDataEntries[idx]}\n{rawDataEntries[idx + 1]}"

                recordDataEntries = self._dataEntryMapper.map(recordData)
                dataEntries += recordDataEntries

                step = 2

            else:
                step = 1

        return dataEntries
