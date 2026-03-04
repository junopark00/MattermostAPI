"""
Mattermost Bots API endpoint module.

Provides bot CRUD, enable/disable, and icon management.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

from .. import constants
from ..Models.bot import Bot
from .base import BaseEndpoint


class BotsEndpoint(BaseEndpoint):
    """
    Mattermost Bots API.

    Examples:
        bot = client.bots.create(
            username="alert-bot",
            display_name="Alert Bot",
        )
    """

    def create(
        self,
        username: str,
        display_name: str = "",
        description: str = "",
    ) -> Bot:
        """
        Create a new bot.

        Args:
            username: Bot username.
            display_name: Display name.
            description: Bot description.

        Returns:
            Created Bot instance.
        """
        body: dict[str, Any] = {"username": username}
        if display_name:
            body["display_name"] = display_name
        if description:
            body["description"] = description

        data = self._http.post(constants.ENDPOINT_BOTS, data=body)
        return Bot.from_dict(data)

    def get_list(
        self,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
        include_deleted: bool = False,
    ) -> list[Bot]:
        """
        List bots with pagination.

        Args:
            page: Page number (0-based).
            per_page: Items per page.
            include_deleted: Include deleted bots.

        Returns:
            List of Bot instances.
        """
        extra: dict[str, Any] = {}
        if include_deleted:
            extra["include_deleted"] = "true"

        params = self._build_pagination_params(
            page=page, per_page=per_page, extra_params=extra
        )
        data = self._http.get(constants.ENDPOINT_BOTS, params=params)
        return Bot.from_list(data)

    def get_by_id(self, bot_user_id: str) -> Bot:
        """Get a bot by user ID. Returns a Bot instance."""
        data = self._http.get(
            constants.ENDPOINT_BOT_BY_ID.format(bot_user_id=bot_user_id)
        )
        return Bot.from_dict(data)

    def update(self, bot_user_id: str, **kwargs: Any) -> Bot:
        """
        Update bot information.

        Args:
            bot_user_id: Bot user ID.
            **kwargs: Fields to update (username, display_name, description).

        Returns:
            Updated Bot instance.
        """
        data = self._http.put(
            constants.ENDPOINT_BOT_BY_ID.format(bot_user_id=bot_user_id),
            data=kwargs,
        )
        return Bot.from_dict(data)

    def disable(self, bot_user_id: str) -> Bot:
        """Disable a bot. Returns the disabled Bot instance."""
        data = self._http.post(
            constants.ENDPOINT_BOT_DISABLE.format(bot_user_id=bot_user_id)
        )
        return Bot.from_dict(data)

    def enable(self, bot_user_id: str) -> Bot:
        """Enable a bot. Returns the enabled Bot instance."""
        data = self._http.post(
            constants.ENDPOINT_BOT_ENABLE.format(bot_user_id=bot_user_id)
        )
        return Bot.from_dict(data)

    def assign_to_user(self, bot_user_id: str, user_id: str) -> Bot:
        """Reassign bot ownership. Returns the updated Bot instance."""
        data = self._http.post(
            constants.ENDPOINT_BOT_ASSIGN.format(
                bot_user_id=bot_user_id, user_id=user_id
            )
        )
        return Bot.from_dict(data)

    def set_icon(
        self,
        bot_user_id: str,
        icon_path: Union[str, Path],
    ) -> bool:
        """Set the bot icon image. Returns True on success."""
        self._http.upload_file(
            constants.ENDPOINT_BOT_ICON.format(bot_user_id=bot_user_id),
            file_path=icon_path,
            file_field_name="image",
        )
        return True

    def delete_icon(self, bot_user_id: str) -> bool:
        """Delete the bot icon image. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_BOT_ICON.format(bot_user_id=bot_user_id)
        )
        return True
