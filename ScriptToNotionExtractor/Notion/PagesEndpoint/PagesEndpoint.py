from Notion.NotionConnector import NotionConnector

from typing import Dict

class PagesEndpoint(object):
    def __init__(self):
        self.__m_httpClient = NotionConnector().HttpClient

    def CreatePageAtDatabase(self, databaseId: str, pageTitle: str) -> str:
        headers = {"Content-Type": "application/json"}
        content = self.__m_httpClient.RunPost("https://api.notion.com/v1/pages", headers=headers, data={
            "parent": { "database_id": databaseId },
            "properties": {
		        "Name": {
                    "title": [{ "text": { "content": pageTitle } } ]
                }
            }
        })
        return content["id"]
    
    def GetPage(self, pageId: str) -> Dict:
        url = f"https://api.notion.com/v1/pages/{pageId}"
        content = self.__m_httpClient.RunGet(url)
        return content
    
    
    def GetPageProperty(self, pageId: str, propertyName: str) -> Dict:
        url = f"https://api.notion.com/v1/pages/{pageId}/properties/{propertyName}"
        content = self.__m_httpClient.RunGet(url)
        return content
    

    def ArchivePage(self, pageId: str) -> None:
        headers = {"Content-Type": "application/json"}
        self.__m_httpClient.RunPost(f"https://api.notion.com/v1/pages/{pageId}", headers=headers, data={
            "archived": True 
        })