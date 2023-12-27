from PdfParser.PdfPage import PdfPage

from pdf2image.pdf2image import convert_from_path, pdfinfo_from_path, counter_generator
from PIL.Image import Image

import os


class PdfParser():
    def __init__(self, pdfFile: str):
        if not os.path.exists(pdfFile) or not pdfFile.endswith(".pdf"):
            raise FileNotFoundError(f"The file '{os.path.abspath(pdfFile)}' is not a valid PDF file.")
        self.__m_pdfFile = pdfFile
        self.__m_nextPageIdx = 0
        self.__m_pdfInfo = pdfinfo_from_path(self.__m_pdfFile)
        self.__m_nextPage = None

    def __iter__(self):
        self.__m_nextPageIdx = 0
        self.__m_nextPage = self.GetPage(self.__m_nextPageIdx)
        self.__m_nextPageIdx += 1
        return self

    def __next__(self) -> PdfPage:
        if self.__m_nextPage == None:
            raise StopIteration
        page = self.__m_nextPage
        self.__m_nextPage = self.GetPage(self.__m_nextPageIdx)
        self.__m_nextPageIdx += 1
        return page
    
    def ParsePagesAsImages(self, imagesPath: str) -> list[str]:
        pdfName = os.path.basename(self.__m_pdfFile).split(".pdf")[0]
        return convert_from_path(self.__m_pdfFile, 
                          output_folder=imagesPath,
                          output_file=counter_generator(pdfName),
                          dpi=200, fmt="png", paths_only=True)

    def GetPage(self, pageIndex: int) -> PdfPage:
        if pageIndex >= self.__m_pdfInfo["Pages"]:
            return None
        pdfPage = PdfPage()
        pageNumber = pageIndex + 1
        pageImages = convert_from_path(self.__m_pdfFile, dpi=200, first_page=pageNumber, last_page=pageNumber + 1)
        pdfPage.images.append(pageImages[0])
        return pdfPage