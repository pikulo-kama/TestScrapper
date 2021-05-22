from typing import List

from pdfplumber import open as pdfopen
from pdfplumber.page import Page

from abstract.pdf import PDFParser, PDFFormatter


class PDFParserImpl(PDFParser):
    _pages: List[Page]
    _pdfFormatter: PDFFormatter

    def __init__(self, pdfFormatter: PDFFormatter) -> None:
        self._pdfFormatter = pdfFormatter

    def parseDocument(self, documentPath: str) -> None:
        self._pages = pdfopen(documentPath).pages

    def getPageFormatted(self, pageNumber: int) -> str:
        return self._pdfFormatter.formatPage(self._pages[pageNumber])

    def getAllPagesFormatted(self, offset: int = 0, limit: int = None) -> List[str]:
        intersectedPages = self._pages[offset:offset + limit] if limit is not None else self._pages[offset:]
        return [self._pdfFormatter.formatPage(page) for page in intersectedPages]
