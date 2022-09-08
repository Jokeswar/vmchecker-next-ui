from urllib.parse import urljoin

import requests


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
