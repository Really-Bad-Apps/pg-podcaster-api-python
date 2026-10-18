"""Synchronous client (requests)."""

from typing import Any, Dict

import requests

from .config import ClientConfig
from .exceptions import raise_for_status


class PgPodcasterClient:
    """Synchronous client for the podcaster portal REST API."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._session = requests.Session()
        self._session.headers.update(config.headers())

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> "PgPodcasterClient":
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def _get(self, path: str) -> Dict[str, Any]:
        response = self._session.get(self._config.url(path), timeout=self._config.timeout_seconds)
        raise_for_status(response.status_code, response.text)
        return response.json()

    def health(self) -> Dict[str, Any]:
        """GET /health — liveness check, no auth required."""
        return self._get("health")
