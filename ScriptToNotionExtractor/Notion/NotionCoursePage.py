from Notion.DatabaseEndpoint.DatabaseEndpoint import DatabaseEndpoint
from Notion.BlocksEndpoint.BlocksEndpoint import BlocksEndpoint

import logging


NOTION_COURSE_DATABASE_ID = "047a0500-c37f-4d15-bf29-c19e1a11538e"

class NotionCoursePage(object):
    def __init__(self, courseNumber: str):
        self.__m_logger = logging.getLogger()

        self.__m_courseNumber = courseNumber
        self.__m_databaseEP = DatabaseEndpoint(NOTION_COURSE_DATABASE_ID)
        self.__m_courseSiteId = self.DetermineCourseSiteId()
        self.__m_lectureNotesDatabaseId = self.DetermineLectureNotesDatabaseId()


    def PrepareLectureNotesPage(self, overwrite: bool = False, update: bool = False):
        lectureNotesDatabaseId = self.DetermineLectureNotesDatabaseId(self.__m_courseNumber)
        if not self.LectureNotePageExists(lectureNotesDatabaseId):
            self.CreateLectureNotePage(lectureNotesDatabaseId)


    def DetermineCourseSiteId(self) -> str:
        try:
            siteId = self.__m_databaseEP.GetPageIdByPropertyValue(NOTION_COURSE_DATABASE_ID, "Kursnummer", self.__m_courseNumber)
        except Exception as e:
            excMsg = f"Failed to determine Notion course site id for course number \"{self.__m_courseNumber}\"."
            self.__m_logger.error(excMsg)
            raise Exception(excMsg) from e
        self.__m_logger.debug(f"Found Notion course site id for course number \"{self.__m_courseNumber}\": \"{siteId}\"")

    def DetermineLectureNotesDatabaseId(self) -> str:
        blocksEndpoint = BlocksEndpoint()
        pageBlocks = blocksEndpoint.GetPageBlocks(self.__m_courseSiteId)["results"]
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


    def LectureNotePageExists(self, lectureNotesDatabaseId: str) -> bool:
        databaseEndpoint = DatabaseEndpoint()
        return False


    def CreateLectureNotePage(self, lectureNotesDatabaseId: str):
        pass