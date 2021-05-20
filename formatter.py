from abstract.pdf import PDFFormatter
from pdfplumber.page import Page


class PDFFormatterImpl(PDFFormatter):

    def formatPage(self, page: Page) -> str:

        pageLeftColumn = page.crop((0, 50, float(page.width) * .5, page.height - 70)).extract_text()
        pageRightColumn = page.crop((float(page.width) * .5, 50, page.width, float(page.height) - 60)).extract_text()

        if type(pageLeftColumn) is str and type(pageRightColumn) is str:
            return "\n".join([pageLeftColumn, pageRightColumn])

        return ""
