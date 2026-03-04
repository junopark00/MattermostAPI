"""
Mattermost Endpoints package.

Aggregates all API endpoint classes.
"""

from .base import BaseEndpoint
from .bots import BotsEndpoint
from .channels import ChannelsEndpoint
from .emoji import EmojiEndpoint
from .files import FilesEndpoint
from .posts import PostsEndpoint
from .reactions import ReactionsEndpoint
from .teams import TeamsEndpoint
from .users import UsersEndpoint
from .webhooks import WebhooksEndpoint

__all__ = [
    "BaseEndpoint",
    "BotsEndpoint",
    "ChannelsEndpoint",
    "EmojiEndpoint",
    "FilesEndpoint",
    "PostsEndpoint",
    "ReactionsEndpoint",
    "TeamsEndpoint",
    "UsersEndpoint",
    "WebhooksEndpoint",
]
