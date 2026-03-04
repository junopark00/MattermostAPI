"""
Mattermost FileInfo data model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .base import BaseModel


@dataclass
class FileInfo(BaseModel):
    """
    Mattermost file info model.

    Attributes:
        id: File ID.
        user_id: Uploader user ID.
        post_id: Attached post ID.
        channel_id: Channel ID.
        create_at: Created timestamp (Unix ms).
        update_at: Updated timestamp (Unix ms).
        delete_at: Deleted timestamp (0 = not deleted).
        name: Filename.
        extension: File extension.
        size: File size (bytes).
        mime_type: MIME type (e.g. "image/png").
        width: Image width (for image files).
        height: Image height (for image files).
    """

    id: str = ""
    user_id: str = ""
    post_id: str = ""
    channel_id: str = ""
    create_at: int = 0
    update_at: int = 0
    delete_at: int = 0
    name: str = ""
    extension: str = ""
    size: int = 0
    mime_type: str = ""
    width: int = 0
    height: int = 0

    @property
    def is_image(self) -> bool:
        """Whether this is an image file."""
        return self.mime_type.startswith("image/")


@dataclass
class FileUploadResponse(BaseModel):
    """
    File upload response model.

    Attributes:
        file_infos: List of uploaded file info dicts.
        client_ids: List of client identifiers.
    """

    file_infos: Optional[list[dict[str, Any]]] = None
    client_ids: Optional[list[str]] = None

    def get_file_infos(self) -> list[FileInfo]:
        """Return a list of FileInfo instances."""
        if not self.file_infos:
            return []
        return FileInfo.from_list(self.file_infos)

    def get_file_ids(self) -> list[str]:
        """Return a list of uploaded file IDs."""
        return [fi["id"] for fi in (self.file_infos or []) if "id" in fi]
