"""
Mattermost API custom exceptions.

Defines granular exceptions for various errors from the Mattermost API,
based on the official error response format.
"""

from __future__ import annotations

from typing import Any, Optional


class MattermostError(Exception):
    """
    Base class for all Mattermost exceptions.

    Attributes:
        message: Error description.
    """

    def __init__(self, message: str = "An unknown Mattermost error occurred.") -> None:
        self.message = message
        super().__init__(self.message)


class MattermostApiError(MattermostError):
    """
    Mattermost API response error.

    Official error format:
        {
            "id": "the.error.id",
            "message": "Something went wrong",
            "request_id": "",
            "status_code": 0,
            "is_oauth": false
        }

    Attributes:
        status_code: HTTP response status code.
        error_id: Mattermost error identifier.
        request_id: Unique request ID.
        is_oauth: Whether this is an OAuth-related error.
    """

    def __init__(
        self,
        message: str,
        status_code: int = 0,
        error_id: str = "",
        request_id: str = "",
        is_oauth: bool = False,
    ) -> None:
        self.status_code = status_code
        self.error_id = error_id
        self.request_id = request_id
        self.is_oauth = is_oauth
        super().__init__(message)

    @classmethod
    def from_response(cls, response_data: dict[str, Any], status_code: int) -> MattermostApiError:
        """
        Create an exception instance from an API error response dict.

        Args:
            response_data: API error response JSON dictionary.
            status_code: HTTP status code.

        Returns:
            Parsed MattermostApiError instance.
        """
        return cls(
            message=response_data.get("message", "Unknown API error"),
            status_code=status_code,
            error_id=response_data.get("id", ""),
            request_id=response_data.get("request_id", ""),
            is_oauth=response_data.get("is_oauth", False),
        )

    def __str__(self) -> str:
        parts = [f"[{self.status_code}]"]
        if self.error_id:
            parts.append(f"({self.error_id})")
        parts.append(self.message)
        return " ".join(parts)


class MattermostAuthenticationError(MattermostApiError):
    """Authentication failed (401 Unauthorized)."""

    pass


class MattermostForbiddenError(MattermostApiError):
    """Insufficient permissions (403 Forbidden)."""

    pass


class MattermostNotFoundError(MattermostApiError):
    """Resource not found (404 Not Found)."""

    pass


class MattermostRateLimitError(MattermostApiError):
    """
    Rate limit exceeded (429 Too Many Requests).

    Attributes:
        retry_after: Seconds until retry is allowed (parsed from header).
    """

    def __init__(
        self,
        message: str = "API rate limit exceeded.",
        retry_after: Optional[float] = None,
        **kwargs: Any,
    ) -> None:
        self.retry_after = retry_after
        super().__init__(message, **kwargs)


class MattermostConnectionError(MattermostError):
    """Server connection failed."""

    pass


class MattermostTimeoutError(MattermostError):
    """Request timed out."""

    pass


class MattermostConfigError(MattermostError):
    """Configuration error."""

    pass


class MattermostFileError(MattermostError):
    """File handling error."""

    pass
