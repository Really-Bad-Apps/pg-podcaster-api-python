import asyncio
from unittest.mock import patch

import httpx
import pytest
import requests
from pg_podcaster_models import DashboardSummary

from pg_podcaster_api import AsyncPgPodcasterClient, PgPodcasterClient
from pg_podcaster_api.config import ClientConfig
from pg_podcaster_api.exceptions import PgPodcasterAuthError


def test_sync_dashboard_uses_bearer_and_shared_model() -> None:
    def respond(request: requests.PreparedRequest, **kwargs: object) -> requests.Response:
        assert request.url == "https://example.test/api/v1/dashboard"
        assert request.headers["Authorization"] == "Bearer caller"
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"generated_at":1700000000,"podcasts":[]}'
        return response

    with patch("requests.Session.send", side_effect=respond):
        with PgPodcasterClient(ClientConfig("https://example.test/api/v1", "caller")) as client:
            assert client.dashboard() == DashboardSummary(generated_at=1700000000)


def test_sync_dashboard_preserves_auth_errors() -> None:
    response = requests.Response()
    response.status_code = 401
    response._content = b'{"error":"unauthorized"}'
    with patch("requests.Session.send", return_value=response):
        with PgPodcasterClient(ClientConfig("https://example.test/api/v1")) as client:
            with pytest.raises(PgPodcasterAuthError):
                client.dashboard()


@pytest.mark.parametrize("status", [200, 401])
def test_async_dashboard(status: int) -> None:
    def respond(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://example.test/api/v1/dashboard"
        assert request.headers["Authorization"] == "Bearer caller"
        return httpx.Response(status, json={"generated_at": 1700000000, "podcasts": []})

    async def run() -> None:
        async with AsyncPgPodcasterClient(
            ClientConfig("https://example.test/api/v1", "caller"),
        ) as client:
            await client._client.aclose()
            client._client = httpx.AsyncClient(
                transport=httpx.MockTransport(respond), headers=client._config.headers(),
            )
            if status == 401:
                with pytest.raises(PgPodcasterAuthError):
                    await client.dashboard()
            else:
                assert await client.dashboard() == DashboardSummary(generated_at=1700000000)

    asyncio.run(run())
