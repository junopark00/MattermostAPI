"""
Mattermost Bot data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class Bot(BaseModel):
    """
    Mattermost Bot model.

    Attributes:
        user_id: Associated user ID.
        username: Bot username.
        display_name: Display name.
        description: Bot description.
        owner_id: Owner user ID.
        create_at: Created timestamp.
        update_at: Updated timestamp.
        delete_at: Deleted timestamp (0 = active).
    """

    user_id: str = ""
    username: str = ""
    display_name: str = ""
    description: str = ""
    owner_id: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0

    @property
    def is_active(self) -> bool:
        """Whether the bot is active."""
        return self.delete_at == 0
