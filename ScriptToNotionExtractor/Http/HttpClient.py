from typing import Any

import requests
import json

class HttpClient:
    def __init__(self, authToken: str, defaultHeaders: dict = {}):
        authHeader = { "Authorization": f"Bearer {authToken}" }
        defaultHeaders.update(authHeader)
        self.__defaultHeaders = defaultHeaders.copy()

    def RunGet(self, url: str, data: dict = None, params: dict = None, headers: dict = {}) -> Any:
        response = self.__ExecuteRequest("GET", url, json=data, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(f"[HttpClient][ERROR] GET request to url {url} returned with status code {response.status_code}.")
        if response.headers.get("content-type", None) == None:
            return response.content
        if "application/json" in response.headers["content-type"]:
            return json.loads(response.content)
        return response
    
    def RunPost(self, url: str, data: dict = None, params: dict = None, headers: dict = {}) -> Any:
        response = self.__ExecuteRequest("POST", url, json=data, params=params, headers=headers)
        if response.status_code != 200:
            raise Exception(f"[HttpClient][ERROR] POST request to url {url} returned with status code {response.status_code}.")
        if response.headers.get("content-type", None) == None:
            return response.content
        if "application/json" in response.headers["content-type"]:
            return json.loads(response.content)
        return response

    def __ExecuteRequest(self, requestType: str, url: str, **kwargs) -> requests.Response:
        self.__defaultHeaders.update(kwargs.get("headers", {}))
        kwargs["headers"] = self.__defaultHeaders
        return requests.request(requestType, url, **kwargs)
