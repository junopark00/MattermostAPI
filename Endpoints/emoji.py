"""
Mattermost Emoji API endpoint module.

Provides custom emoji CRUD and search operations.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

from .. import constants
from ..Models.emoji import Emoji
from .base import BaseEndpoint


class EmojiEndpoint(BaseEndpoint):
    """
    Mattermost Emoji API.

    Examples:
        emojis = client.emoji.get_list()
        emoji = client.emoji.get_by_name("custom_emoji")
    """

    def get_list(
        self,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
    ) -> list[Emoji]:
        """
        List custom emoji with pagination.

        Args:
            page: Page number (0-based).
            per_page: Items per page.

        Returns:
            List of Emoji instances.
        """
        params = self._build_pagination_params(page=page, per_page=per_page)
        data = self._http.get(constants.ENDPOINT_EMOJI, params=params)
        return Emoji.from_list(data)

    def get_by_id(self, emoji_id: str) -> Emoji:
        """Get a custom emoji by ID. Returns an Emoji instance."""
        data = self._http.get(
            constants.ENDPOINT_EMOJI_BY_ID.format(emoji_id=emoji_id)
        )
        return Emoji.from_dict(data)

    def get_by_name(self, emoji_name: str) -> Emoji:
        """Get a custom emoji by name (without colons). Returns an Emoji instance."""
        data = self._http.get(
            constants.ENDPOINT_EMOJI_BY_NAME.format(emoji_name=emoji_name)
        )
        return Emoji.from_dict(data)

    def search(self, term: str, prefix_only: bool = False) -> list[Emoji]:
        """
        Search custom emoji.

        Args:
            term: Search term.
            prefix_only: If True, match prefix only.

        Returns:
            List of matching Emoji instances.
        """
        body: dict[str, Any] = {
            "term": term,
            "prefix_only": prefix_only,
        }
        data = self._http.post(constants.ENDPOINT_EMOJI_SEARCH, data=body)
        return Emoji.from_list(data)

    def create(
        self,
        name: str,
        image_path: Union[str, Path],
    ) -> Emoji:
        """
        Create a custom emoji.

        Args:
            name: Emoji name.
            image_path: Path to the emoji image file.

        Returns:
            Created Emoji instance.
        """
        import json
        data = self._http.upload_file(
            constants.ENDPOINT_EMOJI,
            file_path=image_path,
            file_field_name="image",
            additional_data={"emoji": json.dumps({"name": name})},
        )
        return Emoji.from_dict(data)

    def delete(self, emoji_id: str) -> bool:
        """Delete a custom emoji. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_EMOJI_BY_ID.format(emoji_id=emoji_id)
        )
        return True

    def get_image(
        self,
        emoji_id: str,
        save_path: Union[str, Path],
    ) -> Path:
        """Download a custom emoji image. Returns the saved file path."""
        return self._http.download_file(
            constants.ENDPOINT_EMOJI_IMAGE.format(emoji_id=emoji_id),
            save_path=save_path,
        )
