"""
Mattermost endpoint base module.

Provides common functionality (HTTP client reference, pagination helpers)
for all endpoint classes.
"""

from __future__ import annotations

from typing import Any, Optional

from .. import constants
from ..http_client import HttpClient


class BaseEndpoint:
    """
    Base class for all Mattermost API endpoint classes.

    Attributes:
        _http: Shared HttpClient instance.
    """

    def __init__(self, http_client: HttpClient) -> None:
        self._http = http_client

    def _build_pagination_params(
        self,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
        extra_params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Build pagination query parameters.

        Args:
            page: Page number (0-based).
            per_page: Items per page (max 200).
            extra_params: Additional query parameters.

        Returns:
            Constructed query parameters dict.
        """
        per_page = min(per_page, constants.MAX_PER_PAGE)
        params: dict[str, Any] = {
            "page": page,
            "per_page": per_page,
        }
        if extra_params:
            params.update(extra_params)
        return params

    def _get_all_pages(
        self,
        endpoint: str,
        per_page: int = constants.DEFAULT_PER_PAGE,
        extra_params: Optional[dict[str, Any]] = None,
    ) -> list[dict[str, Any]]:
        """
        Iterate through all pages and collect results.

        Args:
            endpoint: API endpoint path.
            per_page: Items per page.
            extra_params: Additional query parameters.

        Returns:
            Combined list of all page results.
        """
        all_results: list[dict[str, Any]] = []
        page = constants.DEFAULT_PAGE

        while True:
            params = self._build_pagination_params(
                page=page,
                per_page=per_page,
                extra_params=extra_params,
            )
            results = self._http.get(endpoint, params=params)

            if not isinstance(results, list) or len(results) == 0:
                break

            all_results.extend(results)

            if len(results) < per_page:
                break

            page += 1

        return all_results
