"""
Mattermost data models package.

Aggregates all API response data models.
"""

from .base import BaseModel
from .bot import Bot
from .channel import Channel, ChannelMember, ChannelStats
from .emoji import Emoji, Reaction
from .file_info import FileInfo, FileUploadResponse
from .post import Post, PostList
from .team import Team, TeamMember, TeamStats
from .user import User, UserStatus
from .webhook import IncomingWebhook, OutgoingWebhook

__all__ = [
    "BaseModel",
    "Bot",
    "Channel",
    "ChannelMember",
    "ChannelStats",
    "Emoji",
    "FileInfo",
    "FileUploadResponse",
    "IncomingWebhook",
    "OutgoingWebhook",
    "Post",
    "PostList",
    "Reaction",
    "Team",
    "TeamMember",
    "TeamStats",
    "User",
    "UserStatus",
]
