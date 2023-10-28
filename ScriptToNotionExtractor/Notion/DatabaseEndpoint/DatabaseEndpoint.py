from Notion.NotionConnector import NotionConnector

class DatabaseEndpoint(object):
    def __init__(self, databaseId: str):
        self.__m_databaseId = databaseId
        self.__m_httpClient = NotionConnector().HttpClient

    def GetPageIdByPropertyValue(self, propertyName: str, propertyValue: str) -> str:
        url = f"https://api.notion.com/v1/databases/{self.__m_databaseId}/query"
        headers = {"Content-Type": "application/json"}
        content = self.__m_httpClient.RunPost(url, headers=headers, data={
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