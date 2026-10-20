"""
Python client library for the Podcast Guru podcaster portal REST API.

Two clients share one surface: `PgPodcasterClient` (synchronous, requests)
and `AsyncPgPodcasterClient` (asynchronous, httpx). The MCP server uses the
async client.
"""

from .async_client import AsyncPgPodcasterClient
from .client import PgPodcasterClient
from .exceptions import (
    PgPodcasterAPIError,
    PgPodcasterAuthError,
    PgPodcasterConfigError,
    PgPodcasterError,
    PgPodcasterNotFound,
)

__version__ = "0.0.3"

__all__ = [
    "AsyncPgPodcasterClient",
    "PgPodcasterClient",
    "PgPodcasterAPIError",
    "PgPodcasterAuthError",
    "PgPodcasterConfigError",
    "PgPodcasterError",
    "PgPodcasterNotFound",
]
