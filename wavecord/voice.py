from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node


class VoiceManager:
    """Manages VOICE_STATE_UPDATE and VOICE_SERVER_UPDATE events for Lavalink."""

    def __init__(self, node: Node) -> None:
        self.node: Node = node
        self._states: dict[int, dict[str, object]] = {}  # guild_id → session_id + event

    async def update_state(self, guild_id: int, session_id: str) -> None:
        """Handles a VOICE_STATE_UPDATE."""
        state = self._states.setdefault(guild_id, {})
        state["session_id"] = session_id
        await self._dispatch_if_ready(guild_id)

    async def update_server(self, guild_id: int, event: dict) -> None:
        """Handles a VOICE_SERVER_UPDATE."""
        state = self._states.setdefault(guild_id, {})
        state["event"] = event
        await self._dispatch_if_ready(guild_id)

    async def _dispatch_if_ready(self, guild_id: int) -> None:
        """Sends the combined voice update to Lavalink if both pieces are available."""
        state = self._states.get(guild_id)
        if not state or "session_id" not in state or "event" not in state:
            return

        payload = {
            "op": "voiceUpdate",
            "guildId": str(guild_id),
            "sessionId": state["session_id"],
            "event": state["event"],
        }

        await self.node.send(payload)
        self._states.pop(guild_id, None)
