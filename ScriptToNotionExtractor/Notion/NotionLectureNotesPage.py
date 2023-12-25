from Notion.DatabaseEndpoint.DatabaseEndpoint import DatabaseEndpoint
from Notion.BlocksEndpoint.BlocksEndpoint import BlocksEndpoint

import logging

class NotionLectureNotesPage():
    def __init__(self, id: str, containingDatabaseId: str):
        self.__m_logger = logging.getLogger()

        self.__m_databaseEP = DatabaseEndpoint(containingDatabaseId)
        self.__m_id = id


    def Exists(self):
        try:
            
            self.__m_logger.info("The lecture note page already exists.")
            return True
        except:
            self.__m_logger.info("The lecture note page does not exist.")
            return False


    def Create(self, overwrite: bool):
        self.__m_logger.info("Creating lecture note page with the title ''...")

        self.__m_logger.info("Created lecture note page with the title '' successfully.")
        
