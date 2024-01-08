from Notion.DatabaseEndpoint.DatabaseEndpoint import DatabaseEndpoint
from Notion.BlocksEndpoint.BlocksEndpoint import BlocksEndpoint
from Notion.PagesEndpoint.PagesEndpoint import PagesEndpoint
from Notion.NotionLectureNotesPage import (NotionLectureNotesPage,
                                           LectureSlide,
                                           HeaderSize)
from Notion.NotionConnector import NotionConnector
from PdfParser.PdfParser import PdfParser

from datetime import datetime

import subprocess
import logging
import os


NOTION_COURSE_DATABASE_ID = "047a0500-c37f-4d15-bf29-c19e1a11538e"
NOTION_COURSE_LECTURE_SLIDES_EXPORT_BASE_PATH = "Script2Notion/res"

class NotionCoursePage(object):
    def __init__(self, notionConnector: NotionConnector, courseNumber: str):
        self.__m_logger = logging.getLogger("Script2Notion")
        self.__m_notionConnector = notionConnector
        self.__m_courseNumber = courseNumber
        self.__m_databaseEP = DatabaseEndpoint(notionConnector, NOTION_COURSE_DATABASE_ID)
        self.__m_coursePageId = self.__DetermineCourseSiteId()
        self.__m_lectureNotesDatabaseId = self.__DetermineLectureNotesDatabaseId()
        self.__m_lectureNotesDatabaseEP = DatabaseEndpoint(notionConnector, self.__m_lectureNotesDatabaseId)


    def PrepareLectureNotesPage(self, title: str, overwrite: bool = False, update: bool = False) -> None:
        if self.__LectureNotePageExists(title) and overwrite == False and update == False:
            raise Exception(f"A lecture note page with the title '{title}' already exists." +
                            " You can overwrite or update it by setting the correct command line flags.")
        if self.__LectureNotePageExists(title) and update == True:
            pass
        elif self.__LectureNotePageExists(title) and overwrite == True:
            PagesEndpoint(self.__m_notionConnector).ArchivePage(self.__m_lectureNotesDatabaseEP.SearchPageIdByProperty("title", title))
            self.__CreateLectureNotePage(title)
        else:
            self.__CreateLectureNotePage(title)

    def UpdateLectureNotesPage(self, title: str, lectureScriptPath: str) -> None:
        lectureNotesPageId = self.__m_lectureNotesDatabaseEP.SearchPageIdByProperty("title", title)
        notionLectureNotesPage = NotionLectureNotesPage(self.__m_notionConnector, lectureNotesPageId, self.__m_lectureNotesDatabaseId)
        exportedSlides = self.__ExportLectureSlides(lectureScriptPath)
        notionLectureNotesPage.AppendTableOfContents()
        notionLectureNotesPage.AppendDivider()
        for slidePath in exportedSlides:
            lectureNotesSlide = LectureSlide(header="Heading", headerSize=HeaderSize.LARGE, image=slidePath)
            notionLectureNotesPage.AppendHeader(lectureNotesSlide.header, lectureNotesSlide.headerSize)
            notionLectureNotesPage.AppendImage(lectureNotesSlide.image)

    def __ExportLectureSlides(self, lectureScriptPath: str) -> list[str]:
        pdfParser = PdfParser(lectureScriptPath)
        courseName = PagesEndpoint(self.__m_notionConnector).GetPageProperty(self.__m_coursePageId, "title")["results"][0]["title"]["plain_text"]
        lectureName = os.path.basename(lectureScriptPath).split(".pdf")[0]
        exportPath = self.__CreateLectureSlidesExportPath(courseName, lectureName)
        exportedSlidesPaths = pdfParser.ParsePagesAsImages(exportPath)
        self.__PublishSlidesToGitHub(exportPath, courseName + " - " + lectureName)
        exportedSlidesGitPaths = []
        for slidePath in exportedSlidesPaths:
            rest, slideFileName = os.path.split(slidePath)
            rest, lectureDir = os.path.split(rest)
            courseDir = os.path.split(rest)[1]
            exportedSlidesGitPaths.append("/".join([NOTION_COURSE_LECTURE_SLIDES_EXPORT_BASE_PATH, courseDir, lectureDir, slideFileName]))
        return exportedSlidesGitPaths

    def __CreateLectureSlidesExportPath(self, courseName: str, lectureName: str) -> str:
        exportPath = os.path.abspath(os.path.join(NOTION_COURSE_LECTURE_SLIDES_EXPORT_BASE_PATH, "".join(x for x in courseName if x.isalnum() or x == " ")))
        if not os.path.exists(exportPath):
            os.mkdir(exportPath)
        exportPath = os.path.abspath(os.path.join(exportPath, "".join(x for x in lectureName if x.isalnum())))
        if not os.path.exists(exportPath):
            os.mkdir(exportPath)
        return exportPath

    def __PublishSlidesToGitHub(self, imagesFolder: str, commitMessageSuffix: str):
        commitMessage = f"[Script2Notion][{datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S')}] Published slide images for \"{commitMessageSuffix}\"."
        subprocess.run(["git", "add", imagesFolder + "/."])
        subprocess.run(["git", "commit", "-m", commitMessage], capture_output=True)
        subprocess.run(["git", "push"], capture_output=True)

    def __DetermineCourseSiteId(self) -> str:
        try:
            siteId = self.__m_databaseEP.SearchPageIdByProperty("Kursnummer", self.__m_courseNumber)
        except Exception as e:
            excMsg = f"Failed to determine Notion site id for course site with number \"{self.__m_courseNumber}\"."
            self.__m_logger.error(excMsg)
            raise Exception(excMsg) from e
        self.__m_logger.debug(f"Found Notion site id for course number \"{self.__m_courseNumber}\": \"{siteId}\"")
        return siteId

    def __DetermineLectureNotesDatabaseId(self) -> str:
        blocksEndpoint = BlocksEndpoint(self.__m_notionConnector)
        pageBlocks = blocksEndpoint.GetPageBlocks(self.__m_coursePageId)["results"]
        for block in pageBlocks:
            if block["type"] != "column_list" or block["has_children"] == False:
                continue
            columns = blocksEndpoint.GetBlockChildren(block["id"])
            for column in columns["results"]:
                if column["type"] != "column" or column["has_children"] == False:
                    continue
                columnChildren = blocksEndpoint.GetBlockChildren(column["id"])
                for columnChild in columnChildren["results"]:
                    if columnChild["type"] != "child_database":
                        continue
                    if columnChild["child_database"]["title"] == "Mitschriften":
                        self.__m_logger.debug(f"Found Notion course notes database id for course number \"{self.__m_courseNumber}\": \"{columnChild['id']}\"")
                        return columnChild["id"]  

    def __LectureNotePageExists(self, pageTitle: str) -> bool:
        try:
            lectureNotePageId = self.__m_lectureNotesDatabaseEP.SearchPageIdByProperty("title", pageTitle)
            self.__m_logger.debug(f"Found Notion site id for lecture note \"{pageTitle}\": \"{lectureNotePageId}\".")
            return True
        except:
            return False
        
    def __CreateLectureNotePage(self, pageTitle: str) -> str:
        self.__m_lectureNotesDatabaseEP.CreatePage(pageTitle)

        