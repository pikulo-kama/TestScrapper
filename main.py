import os
from pathlib import Path

from abstract.pdf import PDFParser
from abstract.xlsx import XLSXExporter
from formatter import PDFFormatterImpl
from mapper import DataEntryMapperImpl
from parser import PDFParserImpl
from service import DataEntryService
from xlsxexporter import XLSXExporterImpl

XLSX_EXPORT_FILE_PATH = "export.xlsx"
PDF_FILE_PATH = "Abstract_Book_from_the_5th_World_Psoriasis_and_Psoriatic_Arthritis.pdf"
CACHE_FILE_PATH = "cache/cached_content.txt"


class Main:

    def __init__(self, parser: PDFParser, dataEntryService: DataEntryService, exporter: XLSXExporter):
        self.__parser = parser
        self.__dataEntryService = dataEntryService
        self.__exporter = exporter

    def main(self, cache: bool = False):

        if cache and os.path.exists(CACHE_FILE_PATH):
            print(f"Extracting formatted pages from {CACHE_FILE_PATH}")
            with open(CACHE_FILE_PATH, "r") as f:
                pdfContent = f.read()

        else:
            print(f"Parsing pages from {PDF_FILE_PATH}")
            self.__parser.parseDocument(PDF_FILE_PATH)

            print("Formatting pages")
            # Skip pages without data
            pdfContent = "\n".join(self.__parser.getAllPagesFormatted(5))

            if cache:
                with open(CACHE_FILE_PATH, "w") as f:
                    f.write(pdfContent)

        print("Splitting and mapping pages to data entries")
        entries = self.__dataEntryService.splitTextInEntries(pdfContent)

        print(f"Exporting data entries to {XLSX_EXPORT_FILE_PATH}")
        self.__exporter.addRows(entries)
        self.__exporter.export()

    @staticmethod
    def createIfNotExists(filename: str):
        filePath = "/".join(filename.split("/")[:-1])
        Path(filePath).mkdir(parents=True, exist_ok=True)


if __name__ == '__main__':
    Main.createIfNotExists(CACHE_FILE_PATH)
    Main.createIfNotExists(XLSX_EXPORT_FILE_PATH)

    exporter = XLSXExporterImpl(XLSX_EXPORT_FILE_PATH)
    dataEntryService = DataEntryService(DataEntryMapperImpl())
    parser = PDFParserImpl(PDFFormatterImpl())

    Main(parser, dataEntryService, exporter).main(cache=True)
