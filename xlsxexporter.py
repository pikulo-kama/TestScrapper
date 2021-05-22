from typing import List

import xlsxwriter

from abstract.xlsx import XLSXExporter
from models import DataEntry


class XLSXExporterImpl(XLSXExporter):

    def __init__(self, exportFile: str):
        self.__rows: List[DataEntry] = []
        self._exportFile = exportFile

    def export(self):

        workbook = xlsxwriter.Workbook(self._exportFile)
        worksheet = workbook.add_worksheet()

        for idx, header in enumerate(["Name", "Affiliation Name", "Person's Location",
                                      "Session Name", "Topic Title", "Presentation Abstract"]):
            worksheet.write(0, idx, header)

        for row, rowData in enumerate(self.__rows):
            for col, data in enumerate(rowData.toArray()):
                worksheet.write(row + 1, col, data)

        workbook.close()

    def addRow(self, row: DataEntry):
        self.__rows.append(row)

    def addRows(self, rows: List[DataEntry]):
        self.__rows += rows
