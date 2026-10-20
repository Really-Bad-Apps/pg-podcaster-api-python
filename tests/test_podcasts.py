"""Both transports preserve the lookup contract using the shared models."""
import asyncio
import json
from unittest.mock import patch

import httpx
import pytest
import requests
from pg_podcaster_models import PodcastInfo, PodcastLookup

from pg_podcaster_api import AsyncPgPodcasterClient, PgPodcasterClient
from pg_podcaster_api.config import ClientConfig


@pytest.mark.parametrize("pending", [False, True])
def test_podcast_transports(pending: bool) -> None:
    expected = PodcastLookup(status="pending", retry_after=3) if pending else PodcastLookup(
        status="found", podcast=PodcastInfo(id="123", name="Example"))
    status = 202 if pending else 200

    def respond_sync(request: requests.PreparedRequest, **kwargs: object) -> requests.Response:
        assert request.url == "https://example.test/api/v1/podcasts/123"
        assert request.headers["Authorization"] == "Bearer caller"
        response = requests.Response()
        response.status_code = status
        response._content = json.dumps(expected.to_dict()).encode()
        return response

    with patch("requests.Session.send", side_effect=respond_sync):
        with PgPodcasterClient(ClientConfig("https://example.test/api/v1", "caller")) as client:
            assert client.podcast("123") == expected

    def respond_async(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://example.test/api/v1/podcasts/123"
        assert request.headers["Authorization"] == "Bearer caller"
        return httpx.Response(status, json=expected.to_dict())

    async def run() -> None:
        async with AsyncPgPodcasterClient(ClientConfig("https://example.test/api/v1", "caller")) as client:
            await client._client.aclose()
            client._client = httpx.AsyncClient(transport=httpx.MockTransport(respond_async), headers=client._config.headers())
            assert await client.podcast("123") == expected

    asyncio.run(run())
