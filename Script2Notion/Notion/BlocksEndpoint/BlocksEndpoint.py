from Notion.NotionConnector import NotionConnector

from typing import Any

class BlocksEndpoint(object):
    def __init__(self, notionConnector: NotionConnector):
        self.__m_httpClient = notionConnector.HttpClient

    def GetPageBlocks(self, pageId: str) -> dict:
        return self.GetBlockChildren(pageId)
    
    def GetBlockChildren(self, blockId: str) -> dict:
        url = f"https://api.notion.com/v1/blocks/{blockId}/children"
        content = self.__m_httpClient.RunGet(url, params={"page_size": 100})
        return content
    
    def AppendBlockChildren(self, parentBlockId: str, child: dict[Any]) -> None:
        url = f"https://api.notion.com/v1/blocks/{parentBlockId}/children"
        headers = { "Content-Type": "application/json" }
        self.__m_httpClient.RunPatch(url, headers=headers, data={"children": [child]})