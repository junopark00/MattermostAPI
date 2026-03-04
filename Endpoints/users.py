"""
Mattermost Users API endpoint module.

Provides user retrieval, search, and profile management.
"""

from __future__ import annotations

from typing import Any, Optional

from .. import constants
from ..Models.user import User, UserStatus
from .base import BaseEndpoint


class UsersEndpoint(BaseEndpoint):
    """
    Mattermost Users API.

    Examples:
        client = MattermostClient(config)
        me = client.users.get_me()
        user = client.users.get_by_username("john.doe")
    """

    # -----------------------------------------------------------------
    # Retrieve
    # -----------------------------------------------------------------

    def get_me(self) -> User:
        """
        Get the currently authenticated user.

        Returns:
            Current User instance.
        """
        data = self._http.get(
            constants.ENDPOINT_USER_BY_ID.format(user_id=constants.ME)
        )
        return User.from_dict(data)

    def get_by_id(self, user_id: str) -> User:
        """Get a user by ID. Returns a User instance."""
        data = self._http.get(
            constants.ENDPOINT_USER_BY_ID.format(user_id=user_id)
        )
        return User.from_dict(data)

    def get_by_username(self, username: str) -> User:
        """Get a user by username. Returns a User instance."""
        data = self._http.get(
            constants.ENDPOINT_USER_BY_USERNAME.format(username=username)
        )
        return User.from_dict(data)

    def get_by_email(self, email: str) -> User:
        """Get a user by email. Returns a User instance."""
        data = self._http.get(
            constants.ENDPOINT_USER_BY_EMAIL.format(email=email)
        )
        return User.from_dict(data)

    def get_list(
        self,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
        in_team: Optional[str] = None,
        in_channel: Optional[str] = None,
    ) -> list[User]:
        """
        List users with pagination.

        Args:
            page: Page number (0-based).
            per_page: Items per page.
            in_team: Filter by team ID.
            in_channel: Filter by channel ID.

        Returns:
            List of User instances.
        """
        extra: dict[str, Any] = {}
        if in_team:
            extra["in_team"] = in_team
        if in_channel:
            extra["in_channel"] = in_channel

        params = self._build_pagination_params(
            page=page, per_page=per_page, extra_params=extra
        )
        data = self._http.get(constants.ENDPOINT_USERS, params=params)
        return User.from_list(data)

    def get_all(
        self,
        in_team: Optional[str] = None,
        in_channel: Optional[str] = None,
    ) -> list[User]:
        """
        Retrieve all users by iterating through all pages.

        Args:
            in_team: Filter by team ID.
            in_channel: Filter by channel ID.

        Returns:
            Complete list of User instances.
        """
        extra: dict[str, Any] = {}
        if in_team:
            extra["in_team"] = in_team
        if in_channel:
            extra["in_channel"] = in_channel

        data = self._get_all_pages(
            constants.ENDPOINT_USERS, extra_params=extra
        )
        return User.from_list(data)

    def get_by_ids(self, user_ids: list[str]) -> list[User]:
        """Bulk-fetch users by a list of IDs. Returns a list of User instances."""
        data = self._http.post(constants.ENDPOINT_USERS_IDS, data=user_ids)
        return User.from_list(data)

    # -----------------------------------------------------------------
    # Search
    # -----------------------------------------------------------------

    def search(self, term: str, **kwargs: Any) -> list[User]:
        """
        Search for users.

        Args:
            term: Search term (username, name, email, etc.).
            **kwargs: Additional options (team_id, in_channel_id, etc.).

        Returns:
            List of matching User instances.
        """
        body: dict[str, Any] = {"term": term}
        body.update(kwargs)
        data = self._http.post(constants.ENDPOINT_USERS_SEARCH, data=body)
        return User.from_list(data)

    def autocomplete(
        self,
        name: str,
        team_id: Optional[str] = None,
        channel_id: Optional[str] = None,
    ) -> list[User]:
        """
        Autocomplete user search.

        Args:
            name: Name or username to search.
            team_id: Scope to team (optional).
            channel_id: Scope to channel (optional).

        Returns:
            List of matching User instances.
        """
        params: dict[str, Any] = {"name": name}
        if team_id:
            params["in_team"] = team_id
        if channel_id:
            params["in_channel"] = channel_id

        data = self._http.get(constants.ENDPOINT_USERS_AUTOCOMPLETE, params=params)
        users_data = data.get("users", []) if isinstance(data, dict) else data
        return User.from_list(users_data)

    # -----------------------------------------------------------------
    # Create / Update
    # -----------------------------------------------------------------

    def create(
        self,
        username: str,
        email: str,
        password: str,
        **kwargs: Any,
    ) -> User:
        """
        Create a new user.

        Args:
            username: Username.
            email: Email address.
            password: Initial password.
            **kwargs: Additional fields (first_name, last_name, nickname, etc.).

        Returns:
            Created User instance.
        """
        body: dict[str, Any] = {
            "username": username,
            "email": email,
            "password": password,
        }
        body.update(kwargs)
        data = self._http.post(constants.ENDPOINT_USERS, data=body)
        return User.from_dict(data)

    def update(self, user_id: str, **kwargs: Any) -> User:
        """
        Update user information.

        Args:
            user_id: Target user ID.
            **kwargs: Fields to update (first_name, last_name, nickname, email, etc.).

        Returns:
            Updated User instance.
        """
        body: dict[str, Any] = {"id": user_id}
        body.update(kwargs)
        data = self._http.put(
            constants.ENDPOINT_USER_BY_ID.format(user_id=user_id),
            data=body,
        )
        return User.from_dict(data)

    def deactivate(self, user_id: str) -> bool:
        """Deactivate (delete) a user. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_USER_BY_ID.format(user_id=user_id)
        )
        return True

    # -----------------------------------------------------------------
    # Status
    # -----------------------------------------------------------------

    def get_status(self, user_id: str) -> UserStatus:
        """Get a user's status. Returns a UserStatus instance."""
        data = self._http.get(
            constants.ENDPOINT_USER_STATUS.format(user_id=user_id)
        )
        return UserStatus.from_dict(data)

    def update_status(self, user_id: str, status: str) -> UserStatus:
        """
        Update a user's status.

        Args:
            user_id: User ID.
            status: New status ("online", "away", "dnd", "offline").

        Returns:
            Updated UserStatus instance.
        """
        data = self._http.put(
            constants.ENDPOINT_USER_STATUS.format(user_id=user_id),
            data={"user_id": user_id, "status": status},
        )
        return UserStatus.from_dict(data)

    def get_statuses_by_ids(self, user_ids: list[str]) -> list[UserStatus]:
        """Bulk-fetch user statuses by IDs. Returns a list of UserStatus instances."""
        data = self._http.post(constants.ENDPOINT_USERS_STATUS_IDS, data=user_ids)
        return UserStatus.from_list(data)

    # -----------------------------------------------------------------
    # Team / Channel Membership
    # -----------------------------------------------------------------

    def get_teams(self, user_id: str) -> list[dict[str, Any]]:
        """Get teams the user belongs to. Returns a list of team info dicts."""
        return self._http.get(
            constants.ENDPOINT_USER_TEAMS.format(user_id=user_id)
        )

    def get_channels_for_team(
        self,
        user_id: str,
        team_id: str,
    ) -> list[dict[str, Any]]:
        """Get channels the user belongs to in a team. Returns a list of channel info dicts."""
        return self._http.get(
            constants.ENDPOINT_USER_CHANNELS.format(
                user_id=user_id, team_id=team_id
            )
        )
