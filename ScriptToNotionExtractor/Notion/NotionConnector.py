from HttpClient import HttpClient

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
        content = self.__httpClient.RunGet(url, headers=self.__headers)
        return content
        

notionConnector = NotionConnector()
siteId = notionConnector.SearchPageId("Theoretische Informatik: Algorithmen Datenstrukturen")
print(f"Found Sites: {len(siteId)}. Showing Last Two Edited Sites:")
print(json.dumps(siteId[:2], indent=4))
siteId = notionConnector.GetPageIdByPropertyValue("047a0500-c37f-4d15-bf29-c19e1a11538e", "Kursnummer", "INFO4345")
print(json.dumps(siteId, indent=4))