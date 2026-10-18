"""Shared configuration for the sync and async clients."""

from dataclasses import dataclass
from typing import Dict, Optional

from .exceptions import PgPodcasterConfigError

DEFAULT_TIMEOUT_SECONDS: float = 30.0


@dataclass(frozen=True)
class ClientConfig:
    """Connection settings shared by both clients.

    `base_url` is the API root without a trailing slash, e.g.
    `https://podcaster.podcastguru.io/api/v1`. `api_key` is sent as a bearer
    token and may be None for unauthenticated endpoints such as health.
    """

    base_url: str
    api_key: Optional[str] = None
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS

    def __post_init__(self) -> None:
        if not self.base_url:
            raise PgPodcasterConfigError("base_url is required")
        if self.base_url.endswith("/"):
            object.__setattr__(self, "base_url", self.base_url.rstrip("/"))

    def headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"
