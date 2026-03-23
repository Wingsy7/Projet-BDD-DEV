import os

import requests


class ClientAPI:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("SCHOOL_API_URL", "http://127.0.0.1:8000")).rstrip("/")

    def request(
        self,
        method: str,
        path: str,
        json_data: dict | None = None,
        params: dict | None = None,
    ):
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, json=json_data, params=params, timeout=30)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            raise RuntimeError(f"HTTP {response.status_code}: {detail}") from exc

        if not response.content:
            return None

        try:
            return response.json()
        except ValueError:
            return response.text
