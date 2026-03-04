"""
Mattermost API configuration module.

Manages Mattermost server connection settings via environment variables
or direct injection. Uses pathlib.Path for cross-platform path handling.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from . import constants


@dataclass
class MattermostConfig:
    """
    Mattermost server connection settings.

    Examples:
        # Create with explicit values
        config = MattermostConfig(
            url="https://mattermost.example.com",
            token="your-personal-access-token",
        )

        # Create from environment variables
        config = MattermostConfig.from_env()

        # Create from .env file
        config = MattermostConfig.from_env_file(Path("/path/to/.env"))
    """

    url: str = ""
    token: str = ""
    scheme: str = constants.DEFAULT_SCHEME
    port: int = constants.DEFAULT_PORT
    base_path: str = constants.API_BASE_PATH
    timeout: int = constants.DEFAULT_TIMEOUT_SECONDS
    verify_ssl: bool = True
    debug: bool = False
    max_retries: int = constants.RATE_LIMIT_MAX_RETRIES
    retry_delay: float = constants.RATE_LIMIT_RETRY_DELAY_SECONDS
    # Session login credentials (when not using token)
    login_id: Optional[str] = None
    password: Optional[str] = None
    mfa_token: Optional[str] = None

    @property
    def base_url(self) -> str:
        """
        Return the full API base URL.

        Returns:
            URL string like "https://mattermost.example.com/api/v4".
        """
        url = self.url.rstrip("/")
        if not url.startswith(("http://", "https://")):
            url = f"{self.scheme}://{url}"
        return f"{url}{self.base_path}"

    @property
    def server_url(self) -> str:
        """Return the server root URL (without API path)."""
        url = self.url.rstrip("/")
        if not url.startswith(("http://", "https://")):
            url = f"{self.scheme}://{url}"
        return url

    @property
    def websocket_url(self) -> str:
        """Return the WebSocket connection URL."""
        server = self.server_url
        ws_scheme = "wss" if server.startswith("https://") else "ws"
        host = server.replace("https://", "").replace("http://", "")
        return f"{ws_scheme}://{host}{constants.ENDPOINT_WEBSOCKET}"

    @classmethod
    def from_env(
        cls,
        prefix: str = "MM_",
    ) -> MattermostConfig:
        """
        Load settings from environment variables.

        Examples:
            # Set env vars then call
            # MM_URL=https://mattermost.example.com
            # MM_TOKEN=your-token
            config = MattermostConfig.from_env()

        Args:
            prefix: Environment variable prefix. Defaults to "MM_".

        Returns:
            MattermostConfig instance initialized from environment variables.
        """
        return cls(
            url=os.environ.get(f"{prefix}URL", ""),
            token=os.environ.get(f"{prefix}TOKEN", ""),
            scheme=os.environ.get(f"{prefix}SCHEME", constants.DEFAULT_SCHEME),
            port=int(os.environ.get(f"{prefix}PORT", str(constants.DEFAULT_PORT))),
            timeout=int(
                os.environ.get(f"{prefix}TIMEOUT", str(constants.DEFAULT_TIMEOUT_SECONDS))
            ),
            verify_ssl=os.environ.get(f"{prefix}VERIFY_SSL", "true").lower() == "true",
            debug=os.environ.get(f"{prefix}DEBUG", "false").lower() == "true",
            login_id=os.environ.get(f"{prefix}LOGIN_ID"),
            password=os.environ.get(f"{prefix}PASSWORD"),
            mfa_token=os.environ.get(f"{prefix}MFA_TOKEN"),
        )

    @classmethod
    def from_env_file(
        cls,
        env_path: Path,
        prefix: str = "MM_",
    ) -> MattermostConfig:
        """
        Load settings from a .env file.

        Examples:
            config = MattermostConfig.from_env_file(Path(".env"))

        Args:
            env_path: Path to the .env file (pathlib.Path).
            prefix: Environment variable prefix. Defaults to "MM_".

        Returns:
            MattermostConfig instance initialized from .env file values.

        Raises:
            FileNotFoundError: If the specified .env file does not exist.
        """
        env_path = Path(env_path).resolve()
        if not env_path.exists():
            raise FileNotFoundError(f".env file not found: {env_path}")

        env_vars: dict[str, str] = {}
        with open(env_path, mode="r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip("\"'")
                    env_vars[key] = value

        return cls(
            url=env_vars.get(f"{prefix}URL", ""),
            token=env_vars.get(f"{prefix}TOKEN", ""),
            scheme=env_vars.get(f"{prefix}SCHEME", constants.DEFAULT_SCHEME),
            port=int(env_vars.get(f"{prefix}PORT", str(constants.DEFAULT_PORT))),
            timeout=int(
                env_vars.get(f"{prefix}TIMEOUT", str(constants.DEFAULT_TIMEOUT_SECONDS))
            ),
            verify_ssl=env_vars.get(f"{prefix}VERIFY_SSL", "true").lower() == "true",
            debug=env_vars.get(f"{prefix}DEBUG", "false").lower() == "true",
            login_id=env_vars.get(f"{prefix}LOGIN_ID"),
            password=env_vars.get(f"{prefix}PASSWORD"),
            mfa_token=env_vars.get(f"{prefix}MFA_TOKEN"),
        )

    def validate(self) -> None:
        """
        Validate required configuration values.

        Raises:
            ValueError: If url is empty or no auth method (token or login_id/password) is set.
        """
        if not self.url:
            raise ValueError("Mattermost server URL is not configured.")

        has_token = bool(self.token)
        has_credentials = bool(self.login_id and self.password)

        if not has_token and not has_credentials:
            raise ValueError(
                "No authentication method configured. "
                "Please set either token or login_id/password."
            )
