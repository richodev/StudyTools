from Notion.NotionConnector import NotionConnector

class SearchEndpoint(object):
    def __init__(self, databaseId: str):
        self.__m_databaseId = databaseId
        self.__m_httpClient = NotionConnector().HttpClient

    def SearchPageId(self, pageName: str) -> List[str]:
        headers = {"Content-Type": "application/json"}
        content = self.__httpClient.RunPost("https://api.notion.com/v1/search", headers=headers, data={
            "query": pageName,
            "sort": {"direction": "descending", 
                     "timestamp": "last_edited_time"}
        })
        return content["results"]