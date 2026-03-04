"""
Mattermost User data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class User(BaseModel):
    """
    Mattermost User model.

    Attributes:
        id: Unique user identifier.
        username: Username.
        email: Email address.
        first_name: First name.
        last_name: Last name.
        nickname: Nickname.
        position: Job title.
        roles: Role string (e.g. "system_user system_admin").
        locale: Locale setting.
        create_at: Created timestamp (Unix ms).
        update_at: Updated timestamp (Unix ms).
        delete_at: Deleted timestamp (0 = not deleted).
    """

    id: str = ""
    username: str = ""
    email: str = ""
    first_name: str = ""
    last_name: str = ""
    nickname: str = ""
    position: str = ""
    roles: str = ""
    locale: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0

    @property
    def is_deleted(self) -> bool:
        """Whether the user is deleted."""
        return self.delete_at > 0

    @property
    def full_name(self) -> str:
        """Full name (first + last)."""
        parts = [p for p in (self.first_name, self.last_name) if p]
        return " ".join(parts)


@dataclass
class UserStatus(BaseModel):
    """
    User status model.

    Attributes:
        user_id: User ID.
        status: Status string (online, away, dnd, offline).
        manual: Whether manually set.
        last_activity_at: Last activity timestamp.
    """

    user_id: str = ""
    status: str = ""
    manual: bool = False
    last_activity_at: int = 0
