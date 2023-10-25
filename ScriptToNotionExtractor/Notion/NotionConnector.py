from typing import List

import requests
import json
import os

class NotionConnector(object):
    def __init__(self, secretToken: str = None):
        if secretToken is None:
            secretToken = os.environ.get("NOTION_TOKEN")
        if secretToken is None:
            raise PermissionError("Notion secret token is not defined.")
        self.__headers = {
            "Authorization": f"Bearer {secretToken}",
            "Notion-Version": "2022-06-28"
        }

    def SearchPageId(self, pageName: str) -> List[str]:
        self.__headers["Content-Type"] = "application/json"
        response = requests.post("https://api.notion.com/v1/search", headers=self.__headers, json={
            "query": pageName,
            "sort": {"direction": "descending", 
                     "timestamp": "last_edited_time"}
        })
        response.raise_for_status()
        return json.loads(response.content)["results"]

notionConnector = NotionConnector()
siteId = notionConnector.SearchPageId("Modellierung und Simulation 1")
print(json.dumps(siteId, indent=4))