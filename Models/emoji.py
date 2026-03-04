"""
Mattermost Emoji and Reaction data models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class Emoji(BaseModel):
    """
    Mattermost custom emoji model.

    Attributes:
        id: Emoji ID.
        creator_id: Creator user ID.
        name: Emoji name (without colons).
        create_at: Created timestamp.
        update_at: Updated timestamp.
        delete_at: Deleted timestamp.
    """

    id: str = ""
    creator_id: str = ""
    name: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0


@dataclass
class Reaction(BaseModel):
    """
    Mattermost Reaction model.

    Attributes:
        user_id: User ID who reacted.
        post_id: Target post ID.
        emoji_name: Emoji name.
        create_at: Created timestamp.
    """

    user_id: str = ""
    post_id: str = ""
    emoji_name: str = ""
    create_at: int = 0
