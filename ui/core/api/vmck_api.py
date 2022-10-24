import base64
from urllib.parse import urljoin
from typing import Union
from enum import Enum

import requests


class VMCheckerJobStatus(Enum):
    NEW = "0"
    WAITING_FOR_RESULTS = "1"
    DONE = "2"
    ERROR = "3"

    @staticmethod
    def from_name(name: str) -> Union[any, None]:
        for enum in VMCheckerJobStatus:
            if enum.name.lower() == name.lower().strip():
                return enum

        return None


class VMCheckerAPI:
    def __init__(self, backend_url: str) -> None:
        self._backend_url = backend_url

    def submit(self, gitlab_private_token: str, gitlab_project_id: int, username: str, archive: str) -> str:
        response = requests.post(
            urljoin(self._backend_url, "submit"),
            data={
                "gitlab_private_token": gitlab_private_token,
                "gitlab_project_id": gitlab_project_id,
                "username": username,
                "archive": archive,
            },
            timeout=5,
        )
        return response.json()["UUID"]

    def retrive_archive(self, gitlab_private_token: str, gitlab_project_id: int) -> str:
        response = requests.post(
            urljoin(self._backend_url, "archive"),
            data={"gitlab_private_token": gitlab_private_token, "gitlab_project_id": gitlab_project_id},
            timeout=5,
        )

        return response.json()["diff"]

    def status(self, job_id: str) -> VMCheckerJobStatus:
        response = requests.get(
            urljoin(self._backend_url, f"{job_id}/status"),
            timeout=5,
        )

        return VMCheckerJobStatus.from_name(response.json()["status"])

    def trace(self, job_id: str) -> str:
        response = requests.get(
            urljoin(self._backend_url, f"{job_id}/trace"),
            timeout=5,
        )

        decoded_bytes = base64.b64decode(response.json()["trace"])

        return str(decoded_bytes, encoding="utf-8")
