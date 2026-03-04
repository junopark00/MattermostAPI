"""
Mattermost Webhooks API endpoint module.

Provides incoming/outgoing webhook CRUD and messaging.
"""

from __future__ import annotations

from typing import Any, Optional

from .. import constants
from ..Models.webhook import IncomingWebhook, OutgoingWebhook
from .base import BaseEndpoint


class WebhooksEndpoint(BaseEndpoint):
    """
    Mattermost Webhooks API.

    Examples:
        hook = client.webhooks.create_incoming(
            channel_id="channel_id",
            display_name="Alert Bot",
        )
        client.webhooks.send_to_incoming(hook.id, text="New alert!")
    """

    # =================================================================
    # Incoming Webhooks
    # =================================================================

    def create_incoming(
        self,
        channel_id: str,
        display_name: str = "",
        description: str = "",
        username: str = "",
        icon_url: str = "",
    ) -> IncomingWebhook:
        """
        Create an incoming webhook.

        Args:
            channel_id: Channel ID for webhook messages.
            display_name: Webhook display name.
            description: Webhook description.
            username: Username override for messages.
            icon_url: Icon URL override for messages.

        Returns:
            Created IncomingWebhook instance.
        """
        body: dict[str, Any] = {"channel_id": channel_id}
        if display_name:
            body["display_name"] = display_name
        if description:
            body["description"] = description
        if username:
            body["username"] = username
        if icon_url:
            body["icon_url"] = icon_url

        data = self._http.post(constants.ENDPOINT_HOOKS_INCOMING, data=body)
        return IncomingWebhook.from_dict(data)

    def get_incoming_list(
        self,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
        team_id: Optional[str] = None,
    ) -> list[IncomingWebhook]:
        """
        List incoming webhooks.

        Args:
            page: Page number (0-based).
            per_page: Items per page.
            team_id: Filter by team (optional).

        Returns:
            List of IncomingWebhook instances.
        """
        extra: dict[str, Any] = {}
        if team_id:
            extra["team_id"] = team_id

        params = self._build_pagination_params(
            page=page, per_page=per_page, extra_params=extra
        )
        data = self._http.get(constants.ENDPOINT_HOOKS_INCOMING, params=params)
        return IncomingWebhook.from_list(data)

    def get_incoming_by_id(self, hook_id: str) -> IncomingWebhook:
        """Get an incoming webhook by ID. Returns an IncomingWebhook instance."""
        data = self._http.get(
            constants.ENDPOINT_HOOK_INCOMING_BY_ID.format(hook_id=hook_id)
        )
        return IncomingWebhook.from_dict(data)

    def update_incoming(self, hook_id: str, **kwargs: Any) -> IncomingWebhook:
        """
        Update an incoming webhook.

        Args:
            hook_id: Webhook ID.
            **kwargs: Fields to update (channel_id, display_name, etc.).

        Returns:
            Updated IncomingWebhook instance.
        """
        body: dict[str, Any] = {"id": hook_id}
        body.update(kwargs)
        data = self._http.put(
            constants.ENDPOINT_HOOK_INCOMING_BY_ID.format(hook_id=hook_id),
            data=body,
        )
        return IncomingWebhook.from_dict(data)

    def delete_incoming(self, hook_id: str) -> bool:
        """Delete an incoming webhook. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_HOOK_INCOMING_BY_ID.format(hook_id=hook_id)
        )
        return True

    # =================================================================
    # Outgoing Webhooks
    # =================================================================

    def create_outgoing(
        self,
        team_id: str,
        display_name: str = "",
        description: str = "",
        channel_id: str = "",
        trigger_words: Optional[list[str]] = None,
        callback_urls: Optional[list[str]] = None,
        trigger_when: int = 0,
        content_type: str = constants.DEFAULT_CONTENT_TYPE,
    ) -> OutgoingWebhook:
        """
        Create an outgoing webhook.

        Args:
            team_id: Team ID.
            display_name: Webhook display name.
            description: Webhook description.
            channel_id: Specific channel ID (optional).
            trigger_words: List of trigger words.
            callback_urls: List of callback URLs.
            trigger_when: Trigger condition (0 = starts with, 1 = contains).
            content_type: Callback request Content-Type.

        Returns:
            Created OutgoingWebhook instance.
        """
        body: dict[str, Any] = {"team_id": team_id}
        if display_name:
            body["display_name"] = display_name
        if description:
            body["description"] = description
        if channel_id:
            body["channel_id"] = channel_id
        if trigger_words:
            body["trigger_words"] = trigger_words
        if callback_urls:
            body["callback_urls"] = callback_urls
        body["trigger_when"] = trigger_when
        body["content_type"] = content_type

        data = self._http.post(constants.ENDPOINT_HOOKS_OUTGOING, data=body)
        return OutgoingWebhook.from_dict(data)

    def get_outgoing_list(
        self,
        page: int = constants.DEFAULT_PAGE,
        per_page: int = constants.DEFAULT_PER_PAGE,
        team_id: Optional[str] = None,
    ) -> list[OutgoingWebhook]:
        """
        List outgoing webhooks.

        Args:
            page: Page number (0-based).
            per_page: Items per page.
            team_id: Filter by team (optional).

        Returns:
            List of OutgoingWebhook instances.
        """
        extra: dict[str, Any] = {}
        if team_id:
            extra["team_id"] = team_id

        params = self._build_pagination_params(
            page=page, per_page=per_page, extra_params=extra
        )
        data = self._http.get(constants.ENDPOINT_HOOKS_OUTGOING, params=params)
        return OutgoingWebhook.from_list(data)

    def get_outgoing_by_id(self, hook_id: str) -> OutgoingWebhook:
        """Get an outgoing webhook by ID. Returns an OutgoingWebhook instance."""
        data = self._http.get(
            constants.ENDPOINT_HOOK_OUTGOING_BY_ID.format(hook_id=hook_id)
        )
        return OutgoingWebhook.from_dict(data)

    def update_outgoing(self, hook_id: str, **kwargs: Any) -> OutgoingWebhook:
        """
        Update an outgoing webhook.

        Args:
            hook_id: Webhook ID.
            **kwargs: Fields to update.

        Returns:
            Updated OutgoingWebhook instance.
        """
        body: dict[str, Any] = {"id": hook_id}
        body.update(kwargs)
        data = self._http.put(
            constants.ENDPOINT_HOOK_OUTGOING_BY_ID.format(hook_id=hook_id),
            data=body,
        )
        return OutgoingWebhook.from_dict(data)

    def delete_outgoing(self, hook_id: str) -> bool:
        """Delete an outgoing webhook. Returns True on success."""
        self._http.delete(
            constants.ENDPOINT_HOOK_OUTGOING_BY_ID.format(hook_id=hook_id)
        )
        return True

    def regenerate_outgoing_token(self, hook_id: str) -> OutgoingWebhook:
        """Regenerate the outgoing webhook token. Returns the updated OutgoingWebhook."""
        data = self._http.post(
            constants.ENDPOINT_HOOK_OUTGOING_REGEN_TOKEN.format(hook_id=hook_id)
        )
        return OutgoingWebhook.from_dict(data)

    # =================================================================
    # Send via Incoming Webhook (direct HTTP call)
    # =================================================================

    def send_to_incoming(
        self,
        webhook_url: str,
        text: str = "",
        channel: str = "",
        username: str = "",
        icon_url: str = "",
        attachments: Optional[list[dict[str, Any]]] = None,
        props: Optional[dict[str, Any]] = None,
    ) -> bool:
        """
        Send a message via an incoming webhook URL.

        This method posts directly to the webhook URL, not through
        the Mattermost REST API.

        Args:
            webhook_url: Full incoming webhook URL.
            text: Message text.
            channel: Channel override (optional).
            username: Username override (optional).
            icon_url: Icon URL override (optional).
            attachments: Message attachments list (optional).
            props: Additional properties (optional).

        Returns:
            True if sent successfully.
        """
        import requests as req

        payload: dict[str, Any] = {}
        if text:
            payload["text"] = text
        if channel:
            payload["channel"] = channel
        if username:
            payload["username"] = username
        if icon_url:
            payload["icon_url"] = icon_url
        if attachments:
            payload["attachments"] = attachments
        if props:
            payload["props"] = props

        response = req.post(
            webhook_url,
            json=payload,
            timeout=self._http._config.timeout,
            verify=self._http._config.verify_ssl,
        )
        return response.status_code == constants.HTTP_OK
