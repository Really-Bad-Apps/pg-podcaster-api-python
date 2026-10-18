import pytest

import pg_podcaster_api
from pg_podcaster_api.config import ClientConfig
from pg_podcaster_api.exceptions import (
    PgPodcasterAPIError,
    PgPodcasterAuthError,
    PgPodcasterConfigError,
    PgPodcasterNotFound,
    raise_for_status,
)


def test_package_imports() -> None:
    assert pg_podcaster_api.__version__


def test_config_strips_trailing_slash_and_builds_urls() -> None:
    config = ClientConfig(base_url="https://example.test/api/v1/", api_key="abc")
    assert config.url("/health") == "https://example.test/api/v1/health"
    assert config.headers()["Authorization"] == "Bearer abc"


def test_config_requires_base_url() -> None:
    with pytest.raises(PgPodcasterConfigError):
        ClientConfig(base_url="")


def test_raise_for_status_maps_codes() -> None:
    raise_for_status(200, "")
    with pytest.raises(PgPodcasterAuthError):
        raise_for_status(401, "")
    with pytest.raises(PgPodcasterNotFound):
        raise_for_status(404, "")
    with pytest.raises(PgPodcasterAPIError):
        raise_for_status(500, "")
