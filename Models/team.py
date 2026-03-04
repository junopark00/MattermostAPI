"""
Mattermost Team data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class Team(BaseModel):
    """
    Mattermost Team model.

    Attributes:
        id: Team ID.
        name: Team name (URL slug).
        display_name: Display name.
        description: Team description.
        email: Team email.
        type: Team type ('O' = open, 'I' = invite-only).
        create_at: Created timestamp (Unix ms).
        update_at: Updated timestamp (Unix ms).
        delete_at: Deleted timestamp (0 = not deleted).
    """

    id: str = ""
    name: str = ""
    display_name: str = ""
    description: str = ""
    email: str = ""
    type: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0

    @property
    def is_deleted(self) -> bool:
        """Whether the team is deleted."""
        return self.delete_at > 0

    @property
    def is_open(self) -> bool:
        """Whether this is an open team."""
        from .. import constants
        return self.type == constants.TEAM_TYPE_OPEN


@dataclass
class TeamMember(BaseModel):
    """
    Team member model.

    Attributes:
        team_id: Team ID.
        user_id: User ID.
        roles: Role string within the team.
        delete_at: Deleted timestamp (0 = active).
    """

    team_id: str = ""
    user_id: str = ""
    roles: str = ""
    delete_at: int = 0


@dataclass
class TeamStats(BaseModel):
    """
    Team statistics model.

    Attributes:
        team_id: Team ID.
        total_member_count: Total member count.
        active_member_count: Active member count.
    """

    team_id: str = ""
    total_member_count: int = 0
    active_member_count: int = 0
