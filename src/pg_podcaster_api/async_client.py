"""Asynchronous client (httpx)."""

from typing import Any, Dict

import httpx
from pg_podcaster_models import DashboardSummary

from .config import ClientConfig
from .exceptions import raise_for_status


class AsyncPgPodcasterClient:
    """Asynchronous client for the podcaster portal REST API."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient(
            headers=config.headers(),
            timeout=config.timeout_seconds,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncPgPodcasterClient":
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()

    async def _get(self, path: str) -> Dict[str, Any]:
        response = await self._client.get(self._config.url(path))
        raise_for_status(response.status_code, response.text)
        return response.json()

    async def health(self) -> Dict[str, Any]:
        """GET /health — liveness check, no auth required."""
        return await self._get("health")

    async def dashboard(self) -> DashboardSummary:
        """GET /dashboard — requires the caller's bearer token."""
        return DashboardSummary.from_dict(await self._get("dashboard"))
