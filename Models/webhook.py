"""
Mattermost Webhook data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class IncomingWebhook(BaseModel):
    """
    Incoming Webhook model.

    Attributes:
        id: Webhook ID.
        create_at: Created timestamp.
        update_at: Updated timestamp.
        delete_at: Deleted timestamp.
        channel_id: Target channel ID.
        team_id: Team ID.
        display_name: Display name.
        description: Description.
        username: Username override for messages.
        icon_url: Icon URL override for messages.
    """

    id: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
    channel_id: str = ""
    team_id: str = ""
    display_name: str = ""
    description: str = ""
    username: str = ""
    icon_url: str = ""


@dataclass
class OutgoingWebhook(BaseModel):
    """
    Outgoing Webhook model.

    Attributes:
        id: Webhook ID.
        create_at: Created timestamp.
        update_at: Updated timestamp.
        delete_at: Deleted timestamp.
        creator_id: Creator user ID.
        channel_id: Target channel ID.
        team_id: Team ID.
        display_name: Display name.
        description: Description.
        trigger_words: List of trigger words.
        trigger_when: Trigger condition (0 = starts with, 1 = contains).
        callback_urls: List of callback URLs.
        content_type: Callback request Content-Type.
    """

    id: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
    creator_id: str = ""
    channel_id: str = ""
    team_id: str = ""
    display_name: str = ""
    description: str = ""
    trigger_words: Optional[list[str]] = None
    trigger_when: int = 0
    callback_urls: Optional[list[str]] = None
    content_type: str = ""
