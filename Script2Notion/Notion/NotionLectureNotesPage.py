from Notion.DatabaseEndpoint.DatabaseEndpoint import DatabaseEndpoint
from Notion.BlocksEndpoint.BlocksEndpoint import BlocksEndpoint

import logging

class NotionLectureNotesPage():
    def __init__(self, id: str, containingDatabaseId: str):
        self.__m_logger = logging.getLogger("Script2Notion")

        self.__m_databaseEP = DatabaseEndpoint(containingDatabaseId)
        self.__m_id = id
                
