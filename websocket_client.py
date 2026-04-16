"""
Mattermost WebSocket client module.

Provides a lightweight async WebSocket client for sending events
to the Mattermost server — primarily the ``user_typing`` action
to display a typing indicator in channels.

This module does NOT provide full event-listening capabilities;
it is designed for fire-and-forget actions such as typing indicators.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Optional

import websockets
from websockets.asyncio.client import ClientConnection

from .config import MattermostConfig

logger = logging.getLogger(__name__)


class MattermostWebSocketClient:
    """
    Lightweight async WebSocket client for Mattermost actions.

    Manages a single WebSocket connection and exposes helper
    methods for sending actions such as ``user_typing``.

    Examples:
        ws = MattermostWebSocketClient(config)
        await ws.connect()
        await ws.typing(channel_id="ch123")
        await ws.close()

    Async context-manager usage:
        async with MattermostWebSocketClient(config) as ws:
            await ws.typing(channel_id="ch123")
    """

    def __init__(self, config: MattermostConfig) -> None:
        self._config = config
        self._ws: Optional[ClientConnection] = None
        self._seq: int = 0

    # -----------------------------------------------------------------
    # Connection lifecycle
    # -----------------------------------------------------------------

    async def connect(self) -> None:
        """
        Open the WebSocket connection and authenticate.

        Raises:
            MattermostError: If authentication fails.
        """
        url = self._config.websocket_url
        logger.debug("Connecting to WebSocket: %s", url)

        self._ws = await websockets.connect(url)

        # Authenticate
        self._seq += 1
        auth_msg = {
            "seq": self._seq,
            "action": "authentication_challenge",
            "data": {"token": self._config.token},
        }
        await self._ws.send(json.dumps(auth_msg))

        # Wait for auth response — may receive a 'hello' event first
        for _ in range(3):
            raw = await self._ws.recv()
            resp = json.loads(raw)
            if resp.get("status") == "OK":
                logger.info("WebSocket authenticated successfully")
                return
            if resp.get("event") == "hello":
                logger.info(
                    "WebSocket connected (server %s)",
                    resp.get("data", {}).get("server_version", "unknown"),
                )
                continue
            logger.warning("WebSocket unexpected response: %s", resp)

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._ws is not None:
            await self._ws.close()
            self._ws = None
            logger.debug("WebSocket connection closed")

    async def __aenter__(self) -> MattermostWebSocketClient:
        await self.connect()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    # -----------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------

    async def _send_action(
        self,
        action: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Send a WebSocket action and return the server reply.

        Args:
            action: Action name (e.g. ``"user_typing"``).
            data: Action payload.

        Returns:
            Server response dict.

        Raises:
            RuntimeError: If the WebSocket is not connected.
        """
        if self._ws is None:
            raise RuntimeError(
                "WebSocket is not connected. Call connect() first."
            )

        self._seq += 1
        msg = {"action": action, "seq": self._seq, "data": data}
        await self._ws.send(json.dumps(msg))

        raw = await self._ws.recv()
        return json.loads(raw)

    async def typing(
        self,
        channel_id: str,
        parent_id: str = "",
    ) -> None:
        """
        Send a typing indicator to a channel.

        Triggers the "user is typing…" indicator visible to
        other members in the channel.

        Args:
            channel_id: Target channel ID.
            parent_id: Parent post ID (for thread typing indicator).
        """
        await self._send_action(
            "user_typing",
            {"channel_id": channel_id, "parent_id": parent_id},
        )
        logger.debug("Typing indicator sent to channel %s", channel_id)
