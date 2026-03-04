"""
Mattermost Teams API endpoint module.

Provides team CRUD and member management.
"""

from __future__ import annotations

from typing import Any, Optional

from .. import constants
from ..Models.team import Team, TeamMember, TeamStats
from .base import BaseEndpoint


class TeamsEndpoint(BaseEndpoint):
    """
    Mattermost Teams API.

    Examples:
        client = MattermostClient(config)
        teams = client.teams.get_all()
        team = client.teams.get_by_name("developers")
    """

    # -----------------------------------------------------------------
    # Retrieve
    # -----------------------------------------------------------------

    def get_by_id(self, team_id: str) -> Team:
        """Get a team by ID. Returns a Team instance."""
        data = self._http.get(
            constants.ENDPOINT_TEAM_BY_ID.format(team_id=team_id)
        )
        return Team.from_dict(data)

    def get_by_name(self, name: str) -> Team:
        """Get a team by name (slug). Returns a Team instance."""
        data = self._http.get(
            constants.ENDPOINT_TEAM_BY_NAME.format(name=name)
        )
        return Team.from_dict(data)

    def get_list(
        self,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
    ) -> list[Team]:
        """
        List teams with pagination.

        Args:
            page: Page number (0-based).
            per_page: Items per page.

        Returns:
            List of Team instances.
        """
        params = self._build_pagination_params(page=page, per_page=per_page)
        data = self._http.get(constants.ENDPOINT_TEAMS, params=params)
        return Team.from_list(data)

    def get_all(self) -> list[Team]:
        """Retrieve all teams by iterating through all pages."""
        data = self._get_all_pages(constants.ENDPOINT_TEAMS)
        return Team.from_list(data)

    def search(self, term: str) -> list[Team]:
        """Search teams by name. Returns a list of matching Team instances."""
        data = self._http.post(
            constants.ENDPOINT_TEAMS_SEARCH,
            data={"term": term},
        )
        return Team.from_list(data)

    # -----------------------------------------------------------------
    # Create / Update / Delete
    # -----------------------------------------------------------------

    def create(
        self,
        name: str,
        display_name: str,
        team_type: str = constants.TEAM_TYPE_OPEN,
        **kwargs: Any,
    ) -> Team:
        """
        Create a new team.

        Args:
            name: Team name (URL slug).
            display_name: Display name.
            team_type: Team type ('O' = open, 'I' = invite-only).
            **kwargs: Additional fields (description, email, etc.).

        Returns:
            Created Team instance.
        """
        body: dict[str, Any] = {
            "name": name,
            "display_name": display_name,
            "type": team_type,
        }
        body.update(kwargs)
        data = self._http.post(constants.ENDPOINT_TEAMS, data=body)
        return Team.from_dict(data)

    def update(self, team_id: str, **kwargs: Any) -> Team:
        """
        Update team information.

        Args:
            team_id: Target team ID.
            **kwargs: Fields to update (display_name, description, etc.).

        Returns:
            Updated Team instance.
        """
        body: dict[str, Any] = {"id": team_id}
        body.update(kwargs)
        data = self._http.put(
            constants.ENDPOINT_TEAM_BY_ID.format(team_id=team_id),
            data=body,
        )
        return Team.from_dict(data)

    def delete(self, team_id: str) -> bool:
        """Soft-delete a team. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_TEAM_BY_ID.format(team_id=team_id)
        )
        return True

    # -----------------------------------------------------------------
    # Member Management
    # -----------------------------------------------------------------

    def get_members(
        self,
        team_id: str,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
    ) -> list[TeamMember]:
        """
        List team members.

        Args:
            team_id: Team ID.
            page: Page number (0-based).
            per_page: Items per page.

        Returns:
            List of TeamMember instances.
        """
        params = self._build_pagination_params(page=page, per_page=per_page)
        data = self._http.get(
            constants.ENDPOINT_TEAM_MEMBERS.format(team_id=team_id),
            params=params,
        )
        return TeamMember.from_list(data)

    def add_member(self, team_id: str, user_id: str) -> TeamMember:
        """
        Add a member to a team.

        Args:
            team_id: Team ID.
            user_id: User ID to add.

        Returns:
            Added TeamMember instance.
        """
        data = self._http.post(
            constants.ENDPOINT_TEAM_MEMBERS.format(team_id=team_id),
            data={"team_id": team_id, "user_id": user_id},
        )
        return TeamMember.from_dict(data)

    def remove_member(self, team_id: str, user_id: str) -> bool:
        """Remove a member from a team. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_TEAM_MEMBER.format(
                team_id=team_id, user_id=user_id
            )
        )
        return True

    def get_members_by_ids(
        self,
        team_id: str,
        user_ids: list[str],
    ) -> list[TeamMember]:
        """Bulk-fetch team members by user IDs. Returns a list of TeamMember instances."""
        data = self._http.post(
            constants.ENDPOINT_TEAM_MEMBERS_IDS.format(team_id=team_id),
            data=user_ids,
        )
        return TeamMember.from_list(data)

    # -----------------------------------------------------------------
    # Statistics
    # -----------------------------------------------------------------

    def get_stats(self, team_id: str) -> TeamStats:
        """Get team statistics. Returns a TeamStats instance."""
        data = self._http.get(
            constants.ENDPOINT_TEAM_STATS.format(team_id=team_id)
        )
        return TeamStats.from_dict(data)
