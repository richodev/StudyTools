from Notion.DatabaseEndpoint.DatabaseEndpoint import DatabaseEndpoint
from Notion.BlocksEndpoint.BlocksEndpoint import BlocksEndpoint
from Notion.PagesEndpoint.PagesEndpoint import PagesEndpoint
from Notion.NotionLectureNotesPage import NotionLectureNotesPage

from typing import Any
import logging


NOTION_COURSE_DATABASE_ID = "047a0500-c37f-4d15-bf29-c19e1a11538e"

class NotionCoursePage(object):
    def __init__(self, courseNumber: str):
        self.__m_logger = logging.getLogger()

        self.__m_courseNumber = courseNumber
        self.__m_databaseEP = DatabaseEndpoint(NOTION_COURSE_DATABASE_ID)
        self.__m_coursePageId = self.__DetermineCourseSiteId()
        self.__m_lectureNotesDatabaseId = self.__DetermineLectureNotesDatabaseId()
        self.__m_lectureNotesDatabaseEP = DatabaseEndpoint(self.__m_lectureNotesDatabaseId)


    def PrepareLectureNotesPage(self, title: str, overwrite: bool = False, update: bool = False):
        if self.__LectureNotePageExists(title) and overwrite == False and update == False:
            raise Exception(f"A lecture note page with the title '{title}' already exists." +
                            " You can overwrite or update it by setting the correct command line flags.")
        if self.__LectureNotePageExists(title) and update == True:
            pass
        elif self.__LectureNotePageExists(title) and overwrite == True:
            PagesEndpoint().ArchivePage(self.__m_lectureNotesDatabaseEP.SearchPageIdByProperty("title", title))
            self.__CreateLectureNotePage(title)
        else:
            self.__CreateLectureNotePage(title)

    def AppendLectureNotesPage(self, title: str, content: Any) -> None:
        lectureNotesPageId = self.__m_lectureNotesDatabaseEP.SearchPageIdByProperty("title", title)
        notionLectureNotesPage = NotionLectureNotesPage(lectureNotesPageId, self.__m_lectureNotesDatabaseId)


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
        blocksEndpoint = BlocksEndpoint()
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
                        self.__m_logger.debug(f"Notion course site notes database id found: \"{columnChild['id']}\"")
                        return columnChild["id"]
                    

    def __LectureNotePageExists(self, pageTitle: str) -> bool:
        try:
            lectureNotePageId = self.__m_lectureNotesDatabaseEP.SearchPageIdByProperty("title", pageTitle)
            self.__m_logger.debug(f"Found Notion site id for lecture note : '{lectureNotePageId}'.")
            return True
        except:
            return False
        
    def __CreateLectureNotePage(self, pageTitle: str) -> str:
        self.__m_lectureNotesDatabaseEP.CreatePage(pageTitle)

        