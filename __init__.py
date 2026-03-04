"""
Mattermost API Python client package.

A Python wrapper for the Mattermost REST API v4, providing a consistent
interface for users, teams, channels, posts, files, webhooks, bots,
emoji, reactions, and more.

Basic usage:
    from MattermostAPI import MattermostClient, MattermostConfig

    config = MattermostConfig(
        url="https://mattermost.example.com",
        token="your-personal-access-token",
    )
    with MattermostClient(config) as client:
        me = client.users.get_me()
        client.posts.send_message("channel_id", "Hello from Python!")

Docs: https://developers.mattermost.com/api-documentation/
"""

from .client import MattermostClient
from .config import MattermostConfig
from .constants import (
    API_VERSION,
    CHANNEL_TYPE_DIRECT,
    CHANNEL_TYPE_GROUP,
    CHANNEL_TYPE_OPEN,
    CHANNEL_TYPE_PRIVATE,
    STATUS_AWAY,
    STATUS_DND,
    STATUS_OFFLINE,
    STATUS_ONLINE,
    TEAM_TYPE_INVITE,
    TEAM_TYPE_OPEN,
)
from .exceptions import (
    MattermostApiError,
    MattermostAuthenticationError,
    MattermostConfigError,
    MattermostConnectionError,
    MattermostError,
    MattermostFileError,
    MattermostForbiddenError,
    MattermostNotFoundError,
    MattermostRateLimitError,
    MattermostTimeoutError,
)

__version__ = "1.0.0"

__all__ = [
    # Client
    "MattermostClient",
    "MattermostConfig",
    # Constants
    "API_VERSION",
    "CHANNEL_TYPE_DIRECT",
    "CHANNEL_TYPE_GROUP",
    "CHANNEL_TYPE_OPEN",
    "CHANNEL_TYPE_PRIVATE",
    "STATUS_AWAY",
    "STATUS_DND",
    "STATUS_OFFLINE",
    "STATUS_ONLINE",
    "TEAM_TYPE_INVITE",
    "TEAM_TYPE_OPEN",
    # Exceptions
    "MattermostApiError",
    "MattermostAuthenticationError",
    "MattermostConfigError",
    "MattermostConnectionError",
    "MattermostError",
    "MattermostFileError",
    "MattermostForbiddenError",
    "MattermostNotFoundError",
    "MattermostRateLimitError",
    "MattermostTimeoutError",
]
