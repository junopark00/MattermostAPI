"""
Mattermost Post data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class Post(BaseModel):
    """
    Mattermost Post (message) model.

    Attributes:
        id: Post ID.
        create_at: Created timestamp (Unix ms).
        update_at: Updated timestamp (Unix ms).
        delete_at: Deleted timestamp (0 = not deleted).
        user_id: Author user ID.
        channel_id: Channel ID.
        root_id: Thread root post ID (for replies).
        message: Message body.
        type: Post type (empty = regular message).
        props: Additional properties dict.
        hashtags: Hashtag string.
        file_ids: List of attached file IDs.
        is_pinned: Whether the post is pinned.
    """

    id: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
    user_id: str = ""
    channel_id: str = ""
    root_id: str = ""
    message: str = ""
    type: str = ""
    props: Optional[dict[str, Any]] = None
    hashtags: str = ""
    file_ids: Optional[list[str]] = None
    is_pinned: bool = False

    @property
    def is_deleted(self) -> bool:
        """Whether the post is deleted."""
        return self.delete_at > 0

    @property
    def is_reply(self) -> bool:
        """Whether this is a threaded reply."""
        return bool(self.root_id)

    @property
    def has_files(self) -> bool:
        """Whether the post has file attachments."""
        return bool(self.file_ids)


@dataclass
class PostList(BaseModel):
    """
    Post list model.

    Represents the post list response structure from the Mattermost API.

    Attributes:
        order: Ordered list of post IDs.
        posts: Mapping of post ID to post data dict.
    """

    order: Optional[list[str]] = None
    posts: Optional[dict[str, Any]] = None

    def get_posts(self) -> list[Post]:
        """Return Post instances in sorted order."""
        if not self.order or not self.posts:
            return []
        result: list[Post] = []
        for post_id in self.order:
            post_data = self.posts.get(post_id)
            if post_data:
                result.append(Post.from_dict(post_data))
        return result
