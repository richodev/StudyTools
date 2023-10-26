from Notion.NotionConnector import NotionConnector

import logging


NOTION_COURSE_DATABASE_ID = "047a0500-c37f-4d15-bf29-c19e1a11538e"

class NotionCoursePage(object):
    def __init__(self, notionConnector: NotionConnector, logger: logging.Logger):
        self.__m_notionConnector = notionConnector
        self.__m_logger = logger


    def PrepareLectureNotesPage(self, courseNumber: str, overwrite: bool = False, update: bool = False):
        lectureNotesDatabaseId = self.DetermineLectureNotesDatabaseId(courseNumber)
        if not self.LectureNotePageExists(lectureNotesDatabaseId):
            self.CreateLectureNotePage(lectureNotesDatabaseId)


    def DetermineLectureNotesDatabaseId(self, courseNumber: str) -> str:
        siteId = self.__m_notionConnector.GetPageIdByPropertyValue(NOTION_COURSE_DATABASE_ID, "Kursnummer", courseNumber)
        self.__m_logger.debug(f"Notion course site id found for course number \"{courseNumber}\": \"{siteId}\"")
        pageBlocks = self.__m_notionConnector.GetPageBlocks(siteId)["results"]
        for block in pageBlocks:
            if block["type"] != "column_list" or block["has_children"] == False:
                continue
            columns = self.__m_notionConnector.GetBlockChildren(block["id"])
            for column in columns["results"]:
                if column["type"] != "column" or column["has_children"] == False:
                    continue
                columnChildren = self.__m_notionConnector.GetBlockChildren(column["id"])
                for columnChild in columnChildren["results"]:
                    if columnChild["type"] != "child_database":
                        continue
                    if columnChild["child_database"]["title"] == "Mitschriften":
                        self.__m_logger.debug(f"Notion course site notes database id found: \"{columnChild['id']}\"")
                        return columnChild["id"]


    def LectureNotePageExists(self, lectureNotesDatabaseId: str) -> bool:
        return False


    def CreateLectureNotePage(self, lectureNotesDatabaseId: str):
        pass