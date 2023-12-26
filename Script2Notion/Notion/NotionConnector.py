from Http.HttpClient import HttpClient

from typing import List, Dict

import os

class NotionConnector(object):
    __m_instance = None
    __m_httpClient = None

    def __new__(cls, secretToken: str = None):
        if cls.__m_instance is None:
            cls.__m_instance = super(NotionConnector, cls).__new__(cls)
            cls.__m_instance.__InitHttpClient(secretToken)
        return cls.__m_instance
    
    def __InitHttpClient(cls, secretToken: str = None):
        if secretToken is None:
            secretToken = os.environ.get("NOTION_TOKEN")
        if secretToken is None:
            raise PermissionError("Notion secret token is not defined.")
        cls.__m_httpClient = HttpClient(secretToken, defaultHeaders={"Notion-Version": "2022-06-28" })

    @property
    def HttpClient(self) -> HttpClient:
        return self.__m_httpClient