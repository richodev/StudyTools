from Http.HttpClient import HttpClient

from typing import List, Dict

import os

class NotionConnector(object):
    _instance = None

    def __new__(cls, secretToken: str = None):
        if cls._instance is None:
            cls._instance = super(NotionConnector, cls).__new__(cls)
            cls.__InitHttpClient(secretToken)
        return cls._instance
    
    def __InitHttpClient(cls, secretToken: str = None):
        if secretToken is None:
            secretToken = os.environ.get("NOTION_TOKEN")
        if secretToken is None:
            raise PermissionError("Notion secret token is not defined.")
        cls.__m_httpClient = HttpClient(secretToken, defaultHeaders={"Notion-Version": "2022-06-28" })

    @property
    def HttpClient(self) -> HttpClient:
        return self.__m_httpClient