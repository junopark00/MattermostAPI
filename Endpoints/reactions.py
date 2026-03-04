"""
Mattermost Reactions API endpoint module.

Provides post reaction (emoji) add, remove, and list operations.
"""

from __future__ import annotations

from typing import Any

from .. import constants
from ..Models.emoji import Reaction
from .base import BaseEndpoint


class ReactionsEndpoint(BaseEndpoint):
    """
    Mattermost Reactions API.

    Examples:
        client.reactions.add("user_id", "post_id", "+1")
        reactions = client.reactions.get_for_post("post_id")
    """

    def add(self, user_id: str, post_id: str, emoji_name: str) -> Reaction:
        """
        Add a reaction to a post.

        Args:
            user_id: User ID adding the reaction.
            post_id: Target post ID.
            emoji_name: Emoji name (without colons, e.g. "thumbsup").

        Returns:
            Created Reaction instance.
        """
        data = self._http.post(
            constants.ENDPOINT_REACTIONS,
            data={
                "user_id": user_id,
                "post_id": post_id,
                "emoji_name": emoji_name,
            },
        )
        return Reaction.from_dict(data)

    def remove(self, user_id: str, post_id: str, emoji_name: str) -> bool:
        """Remove a reaction from a post. Returns True on success."""
        endpoint = (
            f"{constants.ENDPOINT_USERS}/{user_id}"
            f"/posts/{post_id}/reactions/{emoji_name}"
        )
        self._http.delete(endpoint)
        return True

    def get_for_post(self, post_id: str) -> list[Reaction]:
        """
        Get all reactions for a post.

        Args:
            post_id: Target post ID.

        Returns:
            List of Reaction instances.
        """
        data = self._http.get(
            constants.ENDPOINT_POST_REACTIONS.format(post_id=post_id)
        )
        return Reaction.from_list(data)
