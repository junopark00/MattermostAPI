"""
Mattermost Files API endpoint module.

Provides file upload, download, info retrieval, and thumbnail/preview.
Uses pathlib.Path for cross-platform path handling.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union

from .. import constants
from ..Models.file_info import FileInfo, FileUploadResponse
from .base import BaseEndpoint


class FilesEndpoint(BaseEndpoint):
    """
    Mattermost Files API.

    Examples:
        upload = client.files.upload("channel_id", Path("report.pdf"))
        client.posts.create("channel_id", "Report", file_ids=upload.get_file_ids())
    """

    def upload(
        self,
        channel_id: str,
        file_path: Union[str, Path],
    ) -> FileUploadResponse:
        """
        Upload a file to a channel.

        Args:
            channel_id: Channel ID to upload to.
            file_path: File path (pathlib.Path or string).

        Returns:
            FileUploadResponse instance.
        """
        data = self._http.upload_file(
            constants.ENDPOINT_FILES,
            file_path=file_path,
            additional_data={"channel_id": channel_id},
        )
        return FileUploadResponse.from_dict(data)

    def get_info(self, file_id: str) -> FileInfo:
        """Get file metadata. Returns a FileInfo instance."""
        data = self._http.get(
            constants.ENDPOINT_FILE_INFO.format(file_id=file_id)
        )
        return FileInfo.from_dict(data)

    def get_content(self, file_id: str) -> bytes:
        """Get raw file binary data."""
        return self._http.get_raw(
            constants.ENDPOINT_FILE_BY_ID.format(file_id=file_id)
        )

    def download(
        self,
        file_id: str,
        save_path: Union[str, Path],
    ) -> Path:
        """
        Download a file to local storage.

        Args:
            file_id: File ID.
            save_path: Destination path (pathlib.Path or string).

        Returns:
            Path of the saved file.
        """
        return self._http.download_file(
            constants.ENDPOINT_FILE_BY_ID.format(file_id=file_id),
            save_path=save_path,
        )

    def get_thumbnail(
        self,
        file_id: str,
        save_path: Union[str, Path],
    ) -> Path:
        """Download a file thumbnail (for images). Returns the saved file path."""
        return self._http.download_file(
            constants.ENDPOINT_FILE_THUMBNAIL.format(file_id=file_id),
            save_path=save_path,
        )

    def get_preview(
        self,
        file_id: str,
        save_path: Union[str, Path],
    ) -> Path:
        """Download a file preview. Returns the saved file path."""
        return self._http.download_file(
            constants.ENDPOINT_FILE_PREVIEW.format(file_id=file_id),
            save_path=save_path,
        )

    def get_public_link(self, file_id: str) -> str:
        """Get a public link for a file. Returns the URL string."""
        data = self._http.get(
            constants.ENDPOINT_FILE_LINK.format(file_id=file_id)
        )
        if isinstance(data, dict):
            return data.get("link", "")
        return str(data)
