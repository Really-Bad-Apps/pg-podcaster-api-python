"""Exception hierarchy for the pg-podcaster API client."""

from typing import Optional


class PgPodcasterError(Exception):
    """Base class for every error raised by this library."""


class PgPodcasterConfigError(PgPodcasterError):
    """Client was constructed with missing or invalid configuration."""


class PgPodcasterAPIError(PgPodcasterError):
    """The API returned a non-success HTTP status."""

    def __init__(self, status_code: int, message: str, body: Optional[str] = None) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.body = body


class PgPodcasterAuthError(PgPodcasterAPIError):
    """401 — missing or invalid bearer token."""


class PgPodcasterForbidden(PgPodcasterAPIError):
    """403 — authenticated but not allowed."""


class PgPodcasterNotFound(PgPodcasterAPIError):
    """404 — resource does not exist."""


class PgPodcasterValidationError(PgPodcasterAPIError):
    """422 — request body failed validation."""


def raise_for_status(status_code: int, body: str) -> None:
    """Map an HTTP error status to the matching exception. No-op on 2xx."""
    if 200 <= status_code < 300:
        return
    if status_code == 401:
        raise PgPodcasterAuthError(status_code, "unauthorized", body)
    if status_code == 403:
        raise PgPodcasterForbidden(status_code, "forbidden", body)
    if status_code == 404:
        raise PgPodcasterNotFound(status_code, "not found", body)
    if status_code == 422:
        raise PgPodcasterValidationError(status_code, "validation error", body)
    raise PgPodcasterAPIError(status_code, "request failed", body)
