from Http.HttpClient import HttpClient

from typing import List, Dict

import json
import os

class NotionConnector(object):
    def __init__(self, secretToken: str = None):
        if secretToken is None:
            secretToken = os.environ.get("NOTION_TOKEN")
        if secretToken is None:
            raise PermissionError("Notion secret token is not defined.")
        self.__httpClient = HttpClient(secretToken, defaultHeaders={"Notion-Version": "2022-06-28" })

    def SearchPageId(self, pageName: str) -> List[str]:
        headers = {"Content-Type": "application/json"}
        content = self.__httpClient.RunPost("https://api.notion.com/v1/search", headers=headers, data={
            "query": pageName,
            "sort": {"direction": "descending", 
                     "timestamp": "last_edited_time"}
        })
        return content["results"]
    
    def CreatePage(self, parentId: str, pageTitle: str) -> str:
        headers = {"Content-Type": "application/json"}
        content = self.__httpClient.RunPost("https://api.notion.com/v1/***", headers=headers, data={
            "parent": {"page_id": parentId},
            "pageTitle": pageTitle
        })
        return content["result"]
    
    def GetPageIdByPropertyValue(self, databaseId: str, propertyName: str, propertyValue: str) -> str:
        url = f"https://api.notion.com/v1/databases/{databaseId}/query"
        headers = {"Content-Type": "application/json"}
        content = self.__httpClient.RunPost(url, headers=headers, data={
            "filter": {
                "property": propertyName,
                "rich_text": {
                    "equals": propertyValue
                }
            }
        })
        results = content["results"]
        resultType = content["object"]
        if resultType == "list" and len(results) > 1:
            raise Exception(f"Found more than one page with the property value {propertyValue}.")
        return results[0]["id"]
    
    def GetPage(self, pageId: str) -> Dict:
        url = f"https://api.notion.com/v1/pages/{pageId}"
        content = self.__httpClient.RunGet(url)
        return content
    
    def GetPageProperty(self, pageId: str, propertyName: str) -> Dict:
        url = f"https://api.notion.com/v1/pages/{pageId}/properties/{propertyName}"
        content = self.__httpClient.RunGet(url)
        return content
    
    def GetPageBlocks(self, pageId: str) -> Dict:
        return self.GetBlockChildren(pageId)
    
    def GetBlockChildren(self, blockId: str) -> Dict:
        url = f"https://api.notion.com/v1/blocks/{blockId}/children"
        content = self.__httpClient.RunGet(url, params={"page_size": 100})
        return content