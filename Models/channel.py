"""
Mattermost Channel data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class Channel(BaseModel):
    """
    Mattermost Channel model.

    Attributes:
        id: Channel ID.
        team_id: Team ID.
        type: Channel type ('O'=open, 'P'=private, 'D'=direct, 'G'=group).
        display_name: Display name.
        name: Channel name (URL slug).
        header: Channel header.
        purpose: Channel purpose.
        creator_id: Creator user ID.
        create_at: Created timestamp (Unix ms).
        update_at: Updated timestamp (Unix ms).
        delete_at: Deleted timestamp (0 = not deleted).
        total_msg_count: Total message count.
    """

    id: str = ""
    team_id: str = ""
    type: str = ""
    display_name: str = ""
    name: str = ""
    header: str = ""
    purpose: str = ""
    creator_id: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
    total_msg_count: int = 0

    @property
    def is_deleted(self) -> bool:
        """Whether the channel is deleted."""
        return self.delete_at > 0

    @property
    def is_direct(self) -> bool:
        """Whether this is a direct message channel."""
        from .. import constants
        return self.type == constants.CHANNEL_TYPE_DIRECT

    @property
    def is_group(self) -> bool:
        """Whether this is a group message channel."""
        from .. import constants
        return self.type == constants.CHANNEL_TYPE_GROUP

    @property
    def is_private(self) -> bool:
        """Whether this is a private channel."""
        from .. import constants
        return self.type == constants.CHANNEL_TYPE_PRIVATE


@dataclass
class ChannelMember(BaseModel):
    """
    Channel member model.

    Attributes:
        channel_id: Channel ID.
        user_id: User ID.
        roles: Role string within the channel.
        msg_count: Read message count.
        mention_count: Mention count.
        notify_props: Notification settings.
    """

    channel_id: str = ""
    user_id: str = ""
    roles: str = ""
    msg_count: int = 0
    mention_count: int = 0
    notify_props: Optional[dict[str, Any]] = None


@dataclass
class ChannelStats(BaseModel):
    """
    Channel statistics model.

    Attributes:
        channel_id: Channel ID.
        member_count: Member count.
    """

    channel_id: str = ""
    member_count: int = 0
