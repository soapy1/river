import json
import requests
from typing import List


class Park:
    """API for interacting with Park backend"""

    def __init__(self, url: str):
        self.url = url

    def list_environments(self, namespace: str) -> List[str]:
        request_url = f"{self.url}/{namespace}/"
        response = requests.get(request_url)
        response.raise_for_status()
        data = response.json()
        return data["data"]["environments"]
    
    def list_checkpoints(self, namespace: str, environment: str) -> List[str]:
        request_url = f"{self.url}/{namespace}/{environment}/"
        response = requests.get(request_url)
        response.raise_for_status()
        data = response.json()
        return data["data"]["checkpoints"]
