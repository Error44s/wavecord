from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node


class VoiceManager:
    def __init__(self, node: Node) -> None:
        self.node = node
        self._states: dict[int, dict[str, object]] = {}

    async def update_state(self, guild_id: int, session_id: str) -> None:
        state = self._states.setdefault(guild_id, {})
        state["session_id"] = session_id
        await self._dispatch_if_ready(guild_id)

    async def update_server(self, guild_id: int, event: dict[str, object]) -> None:
        state = self._states.setdefault(guild_id, {})
        state["event"] = event
        await self._dispatch_if_ready(guild_id)

    async def _dispatch_if_ready(self, guild_id: int) -> None:
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
