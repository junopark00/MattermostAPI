"""
Mattermost client facade module.

Unifies all API endpoints into a single entry point for consistent
interaction with the Mattermost server.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

from .config import MattermostConfig
from .Endpoints.bots import BotsEndpoint
from .Endpoints.channels import ChannelsEndpoint
from .Endpoints.emoji import EmojiEndpoint
from .Endpoints.files import FilesEndpoint
from .Endpoints.posts import PostsEndpoint
from .Endpoints.reactions import ReactionsEndpoint
from .Endpoints.teams import TeamsEndpoint
from .Endpoints.users import UsersEndpoint
from .Endpoints.webhooks import WebhooksEndpoint
from .http_client import HttpClient

logger = logging.getLogger(__name__)


class MattermostClient:
    """
    Unified Mattermost API client.

    Exposes domain-specific endpoints as properties and handles
    authentication, session management, and resource cleanup.

    Examples (token auth):
        from MattermostAPI.config import MattermostConfig
        from MattermostAPI.client import MattermostClient

        config = MattermostConfig(
            url="https://mattermost.example.com",
            token="your-personal-access-token",
        )
        client = MattermostClient(config)

        me = client.users.get_me()
        print(f"Logged in as: {me.username}")

        client.posts.send_message("channel_id", "Hello!")
        client.close()

    Examples (session login):
        config = MattermostConfig(
            url="https://mattermost.example.com",
            login_id="admin@example.com",
            password="password123",
        )
        client = MattermostClient(config)
        client.login()  # Session token set automatically

    Examples (context manager):
        with MattermostClient(config) as client:
            client.posts.send_message("channel_id", "Hello!")
        # Session closed automatically

    Examples (environment variables):
        config = MattermostConfig.from_env()
        client = MattermostClient(config)
    """

    def __init__(self, config: MattermostConfig) -> None:
        """
        Initialize MattermostClient.

        Args:
            config: Mattermost server connection settings.

        Raises:
            MattermostConfigError: If config validation fails.
        """
        config.validate()
        self._config = config
        self._http = HttpClient(config)

        # Initialize all endpoint instances eagerly
        self._users = UsersEndpoint(self._http)
        self._teams = TeamsEndpoint(self._http)
        self._channels = ChannelsEndpoint(self._http)
        self._posts = PostsEndpoint(self._http)
        self._files = FilesEndpoint(self._http)
        self._webhooks = WebhooksEndpoint(self._http)
        self._bots = BotsEndpoint(self._http)
        self._reactions = ReactionsEndpoint(self._http)
        self._emoji = EmojiEndpoint(self._http)

        logger.info(
            "MattermostClient initialized: %s", config.server_url
        )

    # =================================================================
    # Endpoint Properties
    # =================================================================

    @property
    def users(self) -> UsersEndpoint:
        """Users API endpoint."""
        return self._users

    @property
    def teams(self) -> TeamsEndpoint:
        """Teams API endpoint."""
        return self._teams

    @property
    def channels(self) -> ChannelsEndpoint:
        """Channels API endpoint."""
        return self._channels

    @property
    def posts(self) -> PostsEndpoint:
        """Posts API endpoint."""
        return self._posts

    @property
    def files(self) -> FilesEndpoint:
        """Files API endpoint."""
        return self._files

    @property
    def webhooks(self) -> WebhooksEndpoint:
        """Webhooks API endpoint."""
        return self._webhooks

    @property
    def bots(self) -> BotsEndpoint:
        """Bots API endpoint."""
        return self._bots

    @property
    def reactions(self) -> ReactionsEndpoint:
        """Reactions API endpoint."""
        return self._reactions

    @property
    def emoji(self) -> EmojiEndpoint:
        """Emoji API endpoint."""
        return self._emoji

    # =================================================================
    # Authentication
    # =================================================================

    def login(
        self,
        login_id: Optional[str] = None,
        password: Optional[str] = None,
        mfa_token: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Perform session-token login.

        Examples:
            user_data = client.login()
            user_data = client.login(
                login_id="admin@example.com",
                password="password123",
            )

        Args:
            login_id: Login ID (falls back to config value).
            password: Password (falls back to config value).
            mfa_token: MFA token (optional).

        Returns:
            Authenticated user info dictionary.
        """
        return self._http.login(
            login_id=login_id,
            password=password,
            mfa_token=mfa_token,
        )

    def logout(self) -> bool:
        """Logout the current session. Returns True on success."""
        return self._http.logout()

    # =================================================================
    # Configuration
    # =================================================================

    @property
    def config(self) -> MattermostConfig:
        """Return the current configuration."""
        return self._config

    @property
    def base_url(self) -> str:
        """Return the API base URL."""
        return self._config.base_url

    @property
    def server_url(self) -> str:
        """Return the server root URL."""
        return self._config.server_url

    # =================================================================
    # Resource Management
    # =================================================================

    def close(self) -> None:
        """Close the HTTP session and release all resources."""
        self._http.close()
        logger.info("MattermostClient closed.")

    def __enter__(self) -> MattermostClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __repr__(self) -> str:
        return f"MattermostClient(url='{self._config.server_url}')"
