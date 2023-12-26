from Notion.NotionConnector import NotionConnector
from Notion.PagesEndpoint.PagesEndpoint import PagesEndpoint

class MultiplePagesError(Exception): ...

class DatabaseEndpoint(object):
    def __init__(self, databaseId: str):
        self.__m_databaseId = databaseId
        self.__m_httpClient = NotionConnector().HttpClient


    def QueryPageObjectsByProperty(self, propertyName: str, propertyValue: str) -> dict:
        url = f"https://api.notion.com/v1/databases/{self.__m_databaseId}/query"
        headers = {"Content-Type": "application/json"}
        data = { 
            "filter": {
                "and": [
                    {
                        "property": propertyName,
                        "rich_text": {
                            "equals": propertyValue
                        }
                    }
                ]
            }
        }
        try:
            content = self.__m_httpClient.RunPost(url, headers=headers, data=data)
            return content
        except Exception as exc:
            raise LookupError(f"Could not find a page with the property '{propertyName}={propertyValue}'" +
                            f" in the database with id {self.__m_databaseId}.") from exc
        

    def SearchPageIdByProperty(self, propertyName: str, propertyValue: str) -> str:
        content = self.QueryPageObjectsByProperty(propertyName, propertyValue)
        results = content["results"]
        resultType = content["object"]
        if resultType == "list" and len(results) > 1:
            raise MultiplePagesError(f"Found more than one page with the property value {propertyValue}.")
        return results[0]["id"]
    
    
    def Contains(self, pageTitle: str) -> bool:
        try:
            self.SearchPageIdByProperty("title", pageTitle)
            return True
        except Exception:
            return False
        

    def CreatePage(self, pageTitle: str) -> str:
        pagesEP = PagesEndpoint()
        return pagesEP.CreatePageAtDatabase(self.__m_databaseId, pageTitle)