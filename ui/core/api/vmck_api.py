from __future__ import annotations

import base64
import logging
from enum import Enum
from typing import Optional
from urllib.parse import urljoin

import requests


log = logging.getLogger(__name__)

class VMCheckerJobStatus(Enum):
    NEW = "0"
    WAITING_FOR_RESULTS = "1"
    DONE = "2"
    ERROR = "3"
    UNKNOWN = "4"   # This means that the client could not retrieve the value from the server or the response was invalid

    @staticmethod
    def from_name(name: str) -> Optional[VMCheckerJobStatus]:
        for enum in VMCheckerJobStatus:
            if enum.name.lower() == name.lower().strip():
                return enum

        return None


class VMCheckerAPI:
    TRACE_RETRIEVE_FAILURE = "Failed to retrieve the trace..."

    def __init__(self, backend_url: str) -> None:
        self._backend_url = backend_url

    def submit(self, gitlab_private_token: str, gitlab_project_id: int, gitlab_branch: str, username: str, archive: str) -> str:
        response = requests.post(
            urljoin(self._backend_url, "submit"),
            data={
                "gitlab_private_token": gitlab_private_token,
                "gitlab_project_id": gitlab_project_id,
                "username": username,
                "archive": archive,
            },
            timeout=10,
        )
        return str(response.json()["UUID"])

    def retrive_archive(self, gitlab_private_token: str, gitlab_project_id: int, gitlab_branch: str) -> str:
        response = requests.post(
            urljoin(self._backend_url, "archive"),
            data={"gitlab_private_token": gitlab_private_token, "gitlab_project_id": gitlab_project_id, "gitlab_branch": gitlab_branch},
            timeout=10,
        )

        return str(response.json()["diff"])

    def status(self, job_id: str) -> VMCheckerJobStatus:
        try :
            response = requests.get(
                urljoin(self._backend_url, f"{job_id}/status"),
                timeout=10,
            )
        except Exception as e:
            log.exception("Failed GET request to status endpoint %s", e)
            return VMCheckerJobStatus.UNKNOWN

        try:
            json_response = response.json()
        except Exception as e:
            log.exception("Failed to parse the status response as json: %s", e)
            return VMCheckerJobStatus.UNKNOWN

        if "status" not in json_response:
            log.error("The json response of status is missing the 'status' key %s", json_response)
            return VMCheckerJobStatus.UNKNOWN

        status_raw_value = json_response["status"]
        status = VMCheckerJobStatus.from_name(status_raw_value)
        if status is None:
            log.error("Unknow status value: %s", status_raw_value)
            return VMCheckerJobStatus.UNKNOWN

        return status

    def trace(self, job_id: str) -> str:
        try:
            response = requests.get(
                urljoin(self._backend_url, f"{job_id}/trace"),
                timeout=10,
            )
        except Exception as e:
            log.exception("Failed GET request to trace endpoint %s", e)
            return VMCheckerAPI.TRACE_RETRIEVE_FAILURE

        try:
            json_response = response.json()
        except Exception as e:
            log.exception("Failed to parse the status response as json: %s", e)
            return VMCheckerAPI.TRACE_RETRIEVE_FAILURE

        if "trace" not in json_response:
            log.error("The json response of trace is missing the 'trace' key: %s", json_response)
            return VMCheckerAPI.TRACE_RETRIEVE_FAILURE


        trace_raw_value = json_response["trace"]
        decoded_bytes = base64.b64decode(trace_raw_value)

        return str(decoded_bytes, encoding="utf-8")
