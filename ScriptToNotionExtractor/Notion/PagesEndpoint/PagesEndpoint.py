from Notion.NotionConnector import NotionConnector

from typing import Dict

class PagesEndpoint(object):
    def __init__(self):
        self.__m_httpClient = NotionConnector().HttpClient

    def CreatePage(self, parentId: str, pageTitle: str) -> str:
        headers = {"Content-Type": "application/json"}
        content = self.__m_httpClient.RunPost("https://api.notion.com/v1/***", headers=headers, data={
            "parent": {"page_id": parentId},
            "pageTitle": pageTitle
        })
        return content["result"]
    
    def GetPage(self, pageId: str) -> Dict:
        url = f"https://api.notion.com/v1/pages/{pageId}"
        content = self.__m_httpClient.RunGet(url)
        return content
    
    def GetPageProperty(self, pageId: str, propertyName: str) -> Dict:
        url = f"https://api.notion.com/v1/pages/{pageId}/properties/{propertyName}"
        content = self.__m_httpClient.RunGet(url)
        return content