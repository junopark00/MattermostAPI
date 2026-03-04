"""
Mattermost HTTP client module.

Wraps the requests library to provide authentication, rate-limit retry,
and error translation through a consistent interface.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any, Optional, Union

import requests

from . import constants
from .config import MattermostConfig
from .exceptions import (
    MattermostApiError,
    MattermostAuthenticationError,
    MattermostConnectionError,
    MattermostForbiddenError,
    MattermostNotFoundError,
    MattermostRateLimitError,
    MattermostTimeoutError,
)

logger = logging.getLogger(__name__)


class HttpClient:
    """
    HTTP client for the Mattermost API.

    Built on requests.Session with auth header management, automatic
    rate-limit retry, and error response translation.

    Examples:
        config = MattermostConfig(
            url="https://mattermost.example.com",
            token="your-token",
        )
        http = HttpClient(config)
        response = http.get("/users/me")
    """

    def __init__(self, config: MattermostConfig) -> None:
        self._config = config
        self._session = requests.Session()
        self._base_url = config.base_url
        self._setup_session()

    def _setup_session(self) -> None:
        """Initialize default session headers and SSL verification."""
        self._session.headers.update({
            "Content-Type": constants.DEFAULT_CONTENT_TYPE,
        })
        self._session.verify = self._config.verify_ssl

        if self._config.token:
            self._set_token(self._config.token)

    def _set_token(self, token: str) -> None:
        """Set the auth token in session headers."""
        self._session.headers.update({
            constants.AUTH_HEADER_KEY: f"{constants.AUTH_BEARER_PREFIX} {token}",
        })

    @property
    def token(self) -> str:
        """Return the current auth token."""
        auth_header = self._session.headers.get(constants.AUTH_HEADER_KEY, "")
        prefix = f"{constants.AUTH_BEARER_PREFIX} "
        if auth_header.startswith(prefix):
            return auth_header[len(prefix):]
        return ""

    @token.setter
    def token(self, value: str) -> None:
        """Update the auth token."""
        self._set_token(value)

    def login(
        self,
        login_id: Optional[str] = None,
        password: Optional[str] = None,
        mfa_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Perform session-token login.

        Examples:
            user = http.login(login_id="admin@example.com", password="password123")
            # Session token is set automatically afterward

        Args:
            login_id: Login ID (email, username, or LDAP ID). Falls back to config value.
            password: Password. Falls back to config value.
            mfa_token: MFA token (optional).

        Returns:
            Authenticated user info dictionary.

        Raises:
            MattermostAuthenticationError: On login failure.
        """
        _login_id = login_id or self._config.login_id
        _password = password or self._config.password
        _mfa_token = mfa_token or self._config.mfa_token

        body: dict[str, Any] = {
            "login_id": _login_id,
            "password": _password,
        }
        if _mfa_token:
            body["token"] = _mfa_token

        url = f"{self._base_url}{constants.ENDPOINT_USERS_LOGIN}"
        response = self._session.post(
            url,
            json=body,
            timeout=self._config.timeout,
        )

        if response.status_code == constants.HTTP_OK:
            token = response.headers.get(constants.TOKEN_HEADER_KEY, "")
            if token:
                self._set_token(token)
                logger.info("Login successful via session token.")
            return response.json()

        self._raise_for_status(response)
        return {}  # unreachable, _raise_for_status always raises

    def logout(self) -> bool:
        """Logout the current session. Returns True on success."""
        try:
            self.post(constants.ENDPOINT_USERS_LOGOUT)
            self._session.headers.pop(constants.AUTH_HEADER_KEY, None)
            logger.info("Logout successful.")
            return True
        except MattermostApiError:
            return False

    def get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Perform a GET request.

        Args:
            endpoint: API endpoint path (e.g. "/users/me").
            params: Query parameters.

        Returns:
            JSON response data.
        """
        return self._request("GET", endpoint, params=params)

    def post(
        self,
        endpoint: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Perform a POST request.

        Args:
            endpoint: API endpoint path.
            data: Request body JSON dictionary.
            params: Query parameters.

        Returns:
            JSON response data.
        """
        return self._request("POST", endpoint, json_data=data, params=params)

    def put(
        self,
        endpoint: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Perform a PUT request.

        Args:
            endpoint: API endpoint path.
            data: Request body JSON dictionary.
            params: Query parameters.

        Returns:
            JSON response data.
        """
        return self._request("PUT", endpoint, json_data=data, params=params)

    def delete(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Perform a DELETE request.

        Args:
            endpoint: API endpoint path.
            params: Query parameters.

        Returns:
            JSON response data.
        """
        return self._request("DELETE", endpoint, params=params)

    def patch(
        self,
        endpoint: str,
        data: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Perform a PATCH request.

        Args:
            endpoint: API endpoint path.
            data: Request body JSON dictionary.
            params: Query parameters.

        Returns:
            JSON response data.
        """
        return self._request("PATCH", endpoint, json_data=data, params=params)

    def upload_file(
        self,
        endpoint: str,
        file_path: Union[str, Path],
        file_field_name: str = "files",
        additional_data: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Upload a file via multipart/form-data.

        All extra fields in *additional_data* are sent as multipart form
        fields alongside the file part.  The session's default
        ``Content-Type`` header is explicitly suppressed so that
        ``requests`` can set the correct ``multipart/form-data`` boundary.

        Different Mattermost endpoints expect different field names:

        - ``POST /files`` – field ``"files"``, ``channel_id`` as form data
        - ``POST /emoji`` – field ``"image"``, ``emoji`` JSON as form data
        - ``POST /bots/{id}/icon`` – field ``"image"``, no extra fields

        Examples:
            result = http.upload_file(
                "/files",
                Path("report.pdf"),
                additional_data={"channel_id": "abc123"},
            )

        Args:
            endpoint: API endpoint path.
            file_path: File path (pathlib.Path or string).
            file_field_name: Multipart field name for the file
                (``"files"`` for file uploads, ``"image"`` for emoji / icons).
            additional_data: Extra key-value pairs sent as multipart form
                fields alongside the file (e.g. ``channel_id``).

        Returns:
            JSON response data.

        Raises:
            MattermostFileError: If the file is not found.
        """
        file_path = Path(file_path).resolve()
        if not file_path.exists():
            from .exceptions import MattermostFileError
            raise MattermostFileError(f"File not found: {file_path}")

        url = f"{self._base_url}{endpoint}"
        # Setting Content-Type to None tells requests' merge_setting()
        # to DROP the session's default "application/json" Content-Type.
        # This allows requests to auto-generate the correct
        # "multipart/form-data; boundary=..." header.
        headers: dict[str, Any] = {"Content-Type": None}

        with open(file_path, "rb") as f:
            files = {file_field_name: (file_path.name, f)}

            response = self._session.post(
                url,
                files=files,
                data=additional_data,
                headers=headers,
                timeout=self._config.timeout,
            )

        return self._process_response(response)

    def download_file(
        self,
        endpoint: str,
        save_path: Union[str, Path],
    ) -> Path:
        """
        Download a file.

        Examples:
            saved = http.download_file(
                "/files/abc123",
                Path("downloads/report.pdf"),
            )

        Args:
            endpoint: API endpoint path.
            save_path: Destination file path (pathlib.Path or string).

        Returns:
            Path of the saved file.
        """
        save_path = Path(save_path).resolve()
        save_path.parent.mkdir(parents=True, exist_ok=True)

        url = f"{self._base_url}{endpoint}"
        response = self._session.get(
            url,
            stream=True,
            timeout=self._config.timeout,
        )

        if response.status_code != constants.HTTP_OK:
            self._raise_for_status(response)

        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        logger.info("File downloaded: %s", save_path)
        return save_path

    def get_raw(self, endpoint: str) -> bytes:
        """
        Perform a GET request and return the raw response bytes.

        Useful for endpoints that return binary data (e.g. file content,
        images) instead of JSON.

        Args:
            endpoint: API endpoint path.

        Returns:
            Raw response body as bytes.
        """
        url = f"{self._base_url}{endpoint}"
        response = self._session.get(url, timeout=self._config.timeout)

        if response.status_code != constants.HTTP_OK:
            self._raise_for_status(response)

        return response.content

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
    ) -> Any:
        """
        Common HTTP request logic with rate-limit retry.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH).
            endpoint: API endpoint path.
            params: Query parameters.
            json_data: Request body JSON dictionary.

        Returns:
            JSON response data.
        """
        url = f"{self._base_url}{endpoint}"
        retries = 0

        while True:
            try:
                if self._config.debug:
                    logger.debug("%s %s params=%s body=%s", method, url, params, json_data)

                response = self._session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    timeout=self._config.timeout,
                )

                # Rate limit handling
                if response.status_code == constants.HTTP_TOO_MANY_REQUESTS:
                    retries += 1
                    if retries > self._config.max_retries:
                        self._raise_for_status(response)

                    retry_after = self._parse_retry_after(response)
                    logger.warning(
                        "Rate limit hit. Retry %d/%d, waiting %.1fs.",
                        retries,
                        self._config.max_retries,
                        retry_after,
                    )
                    time.sleep(retry_after)
                    continue

                return self._process_response(response)

            except requests.ConnectionError as e:
                raise MattermostConnectionError(
                    f"Failed to connect to server: {e}"
                ) from e
            except requests.Timeout as e:
                raise MattermostTimeoutError(
                    f"Request timed out ({self._config.timeout}s): {e}"
                ) from e

    def _process_response(self, response: requests.Response) -> Any:
        """Process HTTP response and return data or raise an exception."""
        if response.status_code == constants.HTTP_NO_CONTENT:
            return {}

        if response.status_code in (constants.HTTP_OK, constants.HTTP_CREATED):
            try:
                return response.json()
            except ValueError:
                return {"status": "ok"}

        self._raise_for_status(response)

    def _raise_for_status(self, response: requests.Response) -> None:
        """Raise an appropriate exception based on the HTTP status code."""
        try:
            error_data = response.json()
        except ValueError:
            error_data = {
                "message": response.text or "Unknown error",
                "status_code": response.status_code,
            }

        status = response.status_code
        error_map = {
            constants.HTTP_UNAUTHORIZED: MattermostAuthenticationError,
            constants.HTTP_FORBIDDEN: MattermostForbiddenError,
            constants.HTTP_NOT_FOUND: MattermostNotFoundError,
        }

        if status == constants.HTTP_TOO_MANY_REQUESTS:
            retry_after = self._parse_retry_after(response)
            raise MattermostRateLimitError(
                message=error_data.get("message", "Rate limit exceeded"),
                retry_after=retry_after,
                status_code=status,
                error_id=error_data.get("id", ""),
                request_id=error_data.get("request_id", ""),
            )

        exception_cls = error_map.get(status, MattermostApiError)
        raise exception_cls.from_response(error_data, status)

    def _parse_retry_after(self, response: requests.Response) -> float:
        """Parse the rate-limit retry delay from response headers."""
        reset_header = response.headers.get(constants.RATE_LIMIT_RESET_HEADER, "")
        if reset_header:
            try:
                return max(float(reset_header), self._config.retry_delay)
            except ValueError:
                pass
        return self._config.retry_delay

    def close(self) -> None:
        """Close the HTTP session."""
        self._session.close()
        logger.info("HTTP session closed.")

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
