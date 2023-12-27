from Notion.DatabaseEndpoint.DatabaseEndpoint import DatabaseEndpoint
from Notion.PagesEndpoint.PagesEndpoint import PagesEndpoint
from Notion.BlocksEndpoint.BlocksEndpoint import BlocksEndpoint
from Notion.NotionConnector import NotionConnector

from dataclasses import dataclass, field
from urllib.parse import quote
from PIL.Image import Image
from enum import Enum

import logging
import os

class HeaderSize(Enum):
    LARGE = "heading_1"
    MEDIUM = "heading_2"
    SMALL = "heading_3"
    BOLD = 3

@dataclass
class LectureSlide():
    image: Image
    header: str = ""
    headerSize: HeaderSize = field(default_factory=lambda: HeaderSize.LARGE)

class NotionLectureNotesPage():
    def __init__(self, notionConnector: NotionConnector, id: str, containingDatabaseId: str):
        self.__m_logger = logging.getLogger("Script2Notion")

        self.__m_databaseEP = DatabaseEndpoint(notionConnector, containingDatabaseId)
        self.__m_pagesEP = PagesEndpoint(notionConnector)
        self.__m_blocksEP = BlocksEndpoint(notionConnector)
        self.__m_id = id

    def GetContent(self) -> dict:
        return self.__m_pagesEP.GetPage(self.__m_id)
        
    def AppendHeader(self, header: str, headerSize: HeaderSize) -> None:
        if headerSize == HeaderSize.BOLD:
            return
        headerBlock = {
            "object": "block",
            "type": headerSize.value,
            headerSize.value: {
                "rich_text": [{
                    "type": "text",
                    "text": {
                        "content": header
                    }
                }],
                "color": "default",
                "is_toggleable": False
            }
        }
        self.__m_blocksEP.AppendBlockChildren(self.__m_id, headerBlock)

    def AppendTableOfContents(self) -> None:
        tocBlock = {
            "object": "block",
            "type": "table_of_contents",
            "table_of_contents": {
                "color": "default"
            }
        }
        self.__m_blocksEP.AppendBlockChildren(self.__m_id, tocBlock)

    def AppendImage(self, imagePath: str) -> None:
        imageBlock = {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {
                    "url": f"https://raw.githubusercontent.com/richodev/StudyTools/master/{quote(imagePath)}?token={os.environ.get('GITHUB_STUDY_TOOLS_TOKEN')}"
                }
            }
        }
        self.__m_blocksEP.AppendBlockChildren(self.__m_id, imageBlock)

    def AppendDivider(self) -> None:
        dividerBlock = {
            "object": "block",
            "type": "divider",
            "divider": {}
        }
        self.__m_blocksEP.AppendBlockChildren(self.__m_id, dividerBlock)