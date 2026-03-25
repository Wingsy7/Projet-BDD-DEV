import os

import requests


class ClientAPI:
    def __init__(self) -> None:
        self.base_url = os.getenv("SCHOOL_API_URL", "http://127.0.0.1:8000").rstrip("/")

    def request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        json_data: dict | None = None,
    ) -> dict | list:
        response = requests.request(
            method,
            f"{self.base_url}{path}",
            params=params,
            json=json_data,
            timeout=20,
        )

        if response.status_code >= 400:
            try:
                data = response.json()
                detail = data.get("detail", response.text)
            except ValueError:
                detail = response.text
            raise RuntimeError(f"HTTP {response.status_code} : {detail}")

        if not response.content:
            return {}

        return response.json()
