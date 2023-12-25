from Notion.NotionConnector import NotionConnector

from typing import Dict

class BlocksEndpoint(object):
    def __init__(self):
        self.__m_httpClient = NotionConnector().HttpClient

    def GetPageBlocks(self, pageId: str) -> Dict:
        return self.GetBlockChildren(pageId)
    
    def GetBlockChildren(self, blockId: str) -> Dict:
        url = f"https://api.notion.com/v1/blocks/{blockId}/children"
        content = self.__m_httpClient.RunGet(url, params={"page_size": 100})
        return content