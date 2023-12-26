from pdfreader.viewer import SimplePDFViewer
from pdfreader.types.objects import Page
from pdfreader import PDFDocument
from .PdfPage import PdfPage

import os

class PdfParser():
    __m_pdfDocument = None

    def __init__(self, pdfFile: str):
        if not os.path.exists(pdfFile) or not pdfFile.endswith(".pdf"):
            raise FileNotFoundError(f"The file '{os.path.abspath(pdfFile)}' is not a valid PDF file.")
        fd = open(pdfFile, "rb")
        self.__m_pdfDocument = PDFDocument(fd)
        self.__m_pdfViewer = SimplePDFViewer(fd)


    def NextPage(self) -> PdfPage:
        pdfPage = PdfPage()
        for canvas in self.__m_pdfViewer:
            pageImages = canvas.images
            pageForms = canvas.forms
            pageText = canvas.text_content
            pageInlineImages = canvas.inline_images
            pageStrings = canvas.strings
            with open("tutorial-sample-content-stream-p1.txt", "w") as f:
                f.write(canvas.text_content)
        return pdfPage