"""
Mattermost Posts API endpoint module.

Provides post (message) CRUD, threading, and pinning operations.
"""

from __future__ import annotations

from typing import Any, Optional

from .. import constants
from ..Models.post import Post, PostList
from .base import BaseEndpoint


class PostsEndpoint(BaseEndpoint):
    """
    Mattermost Posts API.

    Examples:
        client = MattermostClient(config)
        post = client.posts.create("channel_id", "Hello!")
        reply = client.posts.create("channel_id", "Reply", root_id=post.id)
    """

    # -----------------------------------------------------------------
    # Retrieve
    # -----------------------------------------------------------------

    def get_by_id(self, post_id: str) -> Post:
        """
        Get a post by ID.

        Args:
            post_id: Post ID.

        Returns:
            Post instance.
        """
        data = self._http.get(
            constants.ENDPOINT_POST_BY_ID.format(post_id=post_id)
        )
        return Post.from_dict(data)

    def get_for_channel(
        self,
        channel_id: str,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
        since: Optional[int] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> PostList:
        """
        List posts in a channel.

        Examples:
            post_list = client.posts.get_for_channel("channel_id")
            for post in post_list.get_posts():
                print(post.message)

        Args:
            channel_id: Channel ID.
            page: Page number (0-based).
            per_page: Items per page.
            since: Only posts after this timestamp in ms (optional).
            before: Only posts before this post ID (optional).
            after: Only posts after this post ID (optional).

        Returns:
            PostList instance.
        """
        extra: dict[str, Any] = {}
        if since is not None:
            extra["since"] = since
        if before is not None:
            extra["before"] = before
        if after is not None:
            extra["after"] = after

        params = self._build_pagination_params(
            page=page, per_page=per_page, extra_params=extra
        )
        data = self._http.get(
            constants.ENDPOINT_CHANNEL_POSTS.format(channel_id=channel_id),
            params=params,
        )
        return PostList.from_dict(data)

    def get_thread(self, post_id: str) -> PostList:
        """
        Get a post's thread (including replies).

        Args:
            post_id: Root post ID.

        Returns:
            PostList instance.
        """
        data = self._http.get(
            constants.ENDPOINT_POST_THREAD.format(post_id=post_id)
        )
        return PostList.from_dict(data)

    def search(self, team_id: str, terms: str, **kwargs: Any) -> PostList:
        """
        Search posts within a team.

        Args:
            team_id: Team ID.
            terms: Search terms.
            **kwargs: Additional options (is_or_search, include_deleted_channels, etc.).

        Returns:
            PostList of search results.
        """
        body: dict[str, Any] = {"terms": terms}
        body.update(kwargs)
        data = self._http.post(
            constants.ENDPOINT_POSTS_SEARCH.format(team_id=team_id),
            data=body,
        )
        return PostList.from_dict(data)

    # -----------------------------------------------------------------
    # Create / Update / Delete
    # -----------------------------------------------------------------

    def create(
        self,
        channel_id: str,
        message: str,
        root_id: str = "",
        file_ids: Optional[list[str]] = None,
        props: Optional[dict[str, Any]] = None,
    ) -> Post:
        """
        Create a new post (message).

        Examples:
            post = client.posts.create("channel_id", "Hello!")
            reply = client.posts.create("channel_id", "Reply", root_id="parent_id")
            post = client.posts.create("channel_id", "With file", file_ids=["fid"])
            post = client.posts.create(
                "channel_id", "",
                props={"attachments": [{"text": "text", "color": "#FF0000"}]},
            )

        Args:
            channel_id: Target channel ID.
            message: Message body.
            root_id: Parent post ID (for threaded replies).
            file_ids: List of attached file IDs.
            props: Additional properties (attachments, etc.).

        Returns:
            Created Post instance.
        """
        body: dict[str, Any] = {
            "channel_id": channel_id,
            "message": message,
        }
        if root_id:
            body["root_id"] = root_id
        if file_ids:
            body["file_ids"] = file_ids
        if props:
            body["props"] = props

        data = self._http.post(constants.ENDPOINT_POSTS, data=body)
        return Post.from_dict(data)

    def update(self, post_id: str, message: str, **kwargs: Any) -> Post:
        """
        Update a post.

        Args:
            post_id: Target post ID.
            message: Updated message body.
            **kwargs: Additional fields to update.

        Returns:
            Updated Post instance.
        """
        body: dict[str, Any] = {
            "id": post_id,
            "message": message,
        }
        body.update(kwargs)
        data = self._http.put(
            constants.ENDPOINT_POST_BY_ID.format(post_id=post_id),
            data=body,
        )
        return Post.from_dict(data)

    def delete(self, post_id: str) -> bool:
        """Delete a post. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_POST_BY_ID.format(post_id=post_id)
        )
        return True

    # -----------------------------------------------------------------
    # Pin
    # -----------------------------------------------------------------

    def pin(self, post_id: str) -> bool:
        """Pin a post to the channel. Returns True on success."""
        self._http.post(
            constants.ENDPOINT_POST_PIN.format(post_id=post_id)
        )
        return True

    def unpin(self, post_id: str) -> bool:
        """Unpin a post from the channel. Returns True on success."""
        self._http.post(
            constants.ENDPOINT_POST_UNPIN.format(post_id=post_id)
        )
        return True

    # -----------------------------------------------------------------
    # Convenience Methods
    # -----------------------------------------------------------------

    def send_message(
        self,
        channel_id: str,
        message: str,
        **kwargs: Any,
    ) -> Post:
        """
        Send a message (convenience wrapper around create).

        Args:
            channel_id: Target channel ID.
            message: Message body.
            **kwargs: Additional options (root_id, file_ids, props).

        Returns:
            Created Post instance.
        """
        return self.create(channel_id=channel_id, message=message, **kwargs)

    def send_reply(
        self,
        channel_id: str,
        root_id: str,
        message: str,
        **kwargs: Any,
    ) -> Post:
        """
        Send a threaded reply (convenience wrapper around create).

        Args:
            channel_id: Target channel ID.
            root_id: Root post ID of the thread.
            message: Message body.
            **kwargs: Additional options.

        Returns:
            Created Post instance.
        """
        return self.create(
            channel_id=channel_id,
            message=message,
            root_id=root_id,
            **kwargs,
        )
