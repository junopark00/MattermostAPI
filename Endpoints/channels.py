"""
Mattermost Channels API endpoint module.

Provides channel CRUD, member management, and direct/group messaging.
"""

from __future__ import annotations

from typing import Any, Optional

from .. import constants
from ..Models.channel import Channel, ChannelMember, ChannelStats
from .base import BaseEndpoint


class ChannelsEndpoint(BaseEndpoint):
    """
    Mattermost Channels API.

    Examples:
        client = MattermostClient(config)
        channel = client.channels.get_by_name("team_id", "general")
        dm = client.channels.create_direct("user1_id", "user2_id")
    """

    # -----------------------------------------------------------------
    # Retrieve
    # -----------------------------------------------------------------

    def get_by_id(self, channel_id: str) -> Channel:
        """
        Get a channel by ID.

        Args:
            channel_id: Channel ID.

        Returns:
            Channel instance.
        """
        data = self._http.get(
            constants.ENDPOINT_CHANNEL_BY_ID.format(channel_id=channel_id)
        )
        return Channel.from_dict(data)

    def get_by_name(self, team_id: str, channel_name: str) -> Channel:
        """
        Get a channel by team ID and channel name.

        Args:
            team_id: Team ID.
            channel_name: Channel name (URL slug).

        Returns:
            Channel instance.
        """
        data = self._http.get(
            constants.ENDPOINT_TEAM_CHANNEL_BY_NAME.format(
                team_id=team_id, channel_name=channel_name
            )
        )
        return Channel.from_dict(data)

    def get_list_for_team(
        self,
        team_id: str,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
    ) -> list[Channel]:
        """
        List channels for a team.

        Args:
            team_id: Team ID.
            page: Page number (0-based).
            per_page: Items per page.

        Returns:
            List of Channel instances.
        """
        params = self._build_pagination_params(page=page, per_page=per_page)
        data = self._http.get(
            constants.ENDPOINT_TEAM_CHANNELS.format(team_id=team_id),
            params=params,
        )
        return Channel.from_list(data)

    def search_in_team(self, team_id: str, term: str) -> list[Channel]:
        """
        Search channels within a team.

        Args:
            team_id: Team ID.
            term: Search term.

        Returns:
            List of matching Channel instances.
        """
        data = self._http.post(
            constants.ENDPOINT_TEAM_CHANNELS_SEARCH.format(team_id=team_id),
            data={"term": term},
        )
        return Channel.from_list(data)

    # -----------------------------------------------------------------
    # Create / Update / Delete
    # -----------------------------------------------------------------

    def create(
        self,
        team_id: str,
        name: str,
        display_name: str,
        channel_type: str = constants.CHANNEL_TYPE_OPEN,
        **kwargs: Any,
    ) -> Channel:
        """
        Create a new channel.

        Examples:
            channel = client.channels.create(
                team_id="team_id",
                name="new-channel",
                display_name="New Channel",
            )

        Args:
            team_id: Team ID.
            name: Channel name (URL slug).
            display_name: Display name.
            channel_type: Channel type ('O' = open, 'P' = private).
            **kwargs: Additional fields (purpose, header, etc.).

        Returns:
            Created Channel instance.
        """
        body: dict[str, Any] = {
            "team_id": team_id,
            "name": name,
            "display_name": display_name,
            "type": channel_type,
        }
        body.update(kwargs)
        data = self._http.post(constants.ENDPOINT_CHANNELS, data=body)
        return Channel.from_dict(data)

    def update(self, channel_id: str, **kwargs: Any) -> Channel:
        """
        Update channel information.

        Args:
            channel_id: Target channel ID.
            **kwargs: Fields to update (display_name, header, purpose, etc.).

        Returns:
            Updated Channel instance.
        """
        body: dict[str, Any] = {"id": channel_id}
        body.update(kwargs)
        data = self._http.put(
            constants.ENDPOINT_CHANNEL_BY_ID.format(channel_id=channel_id),
            data=body,
        )
        return Channel.from_dict(data)

    def delete(self, channel_id: str) -> bool:
        """Delete (archive) a channel. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_CHANNEL_BY_ID.format(channel_id=channel_id)
        )
        return True

    # -----------------------------------------------------------------
    # Direct / Group Messaging
    # -----------------------------------------------------------------

    def create_direct(self, user_id_1: str, user_id_2: str) -> Channel:
        """
        Create (or retrieve) a 1:1 direct message channel.

        Examples:
            dm = client.channels.create_direct("my_id", "other_id")
            client.posts.create(dm.id, "Hello!")

        Args:
            user_id_1: First user ID.
            user_id_2: Second user ID.

        Returns:
            Direct message Channel instance.
        """
        data = self._http.post(
            constants.ENDPOINT_CHANNELS_DIRECT,
            data=[user_id_1, user_id_2],
        )
        return Channel.from_dict(data)

    def create_group(self, user_ids: list[str]) -> Channel:
        """
        Create a group message channel.

        Args:
            user_ids: List of user IDs (3 or more).

        Returns:
            Group message Channel instance.
        """
        data = self._http.post(
            constants.ENDPOINT_CHANNELS_GROUP,
            data=user_ids,
        )
        return Channel.from_dict(data)

    # -----------------------------------------------------------------
    # Member Management
    # -----------------------------------------------------------------

    def get_members(
        self,
        channel_id: str,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
    ) -> list[ChannelMember]:
        """
        List channel members.

        Args:
            channel_id: Channel ID.
            page: Page number (0-based).
            per_page: Items per page.

        Returns:
            List of ChannelMember instances.
        """
        params = self._build_pagination_params(page=page, per_page=per_page)
        data = self._http.get(
            constants.ENDPOINT_CHANNEL_MEMBERS.format(channel_id=channel_id),
            params=params,
        )
        return ChannelMember.from_list(data)

    def add_member(self, channel_id: str, user_id: str) -> ChannelMember:
        """
        Add a member to a channel.

        Args:
            channel_id: Channel ID.
            user_id: User ID to add.

        Returns:
            Added ChannelMember instance.
        """
        data = self._http.post(
            constants.ENDPOINT_CHANNEL_MEMBERS.format(channel_id=channel_id),
            data={"user_id": user_id},
        )
        return ChannelMember.from_dict(data)

    def remove_member(self, channel_id: str, user_id: str) -> bool:
        """Remove a member from a channel. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_CHANNEL_MEMBER.format(
                channel_id=channel_id, user_id=user_id
            )
        )
        return True

    # -----------------------------------------------------------------
    # Statistics
    # -----------------------------------------------------------------

    def get_stats(self, channel_id: str) -> ChannelStats:
        """Get channel statistics. Returns a ChannelStats instance."""
        data = self._http.get(
            constants.ENDPOINT_CHANNEL_STATS.format(channel_id=channel_id)
        )
        return ChannelStats.from_dict(data)
