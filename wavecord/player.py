from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .exceptions import PlayerNotConnected
from .queue import TrackQueue
from .track import Track

if TYPE_CHECKING:
    from .node import Node
    from discord import VoiceChannel


class WavePlayer:
    def __init__(self, guild_id: int, node: Node) -> None:
        self.guild_id = guild_id
        self.node = node
        self.channel_id: Optional[int] = None
        self.queue: TrackQueue = TrackQueue()
        self.volume = 100
        self.paused = False
        self.current: Optional[Track] = None

    async def connect(self, channel: VoiceChannel) -> None:
        self.channel_id = channel.id
        await self.node.send(
            {
                "op": "voiceUpdate",
                "guildId": self.guild_id,
                "channelId": str(channel.id),
            }
        )

    async def play(self, track: Track) -> None:
        if not self.channel_id:
            raise PlayerNotConnected("Player is not connected to a voice channel.")

        self.current = track
        await self.node.send(
            {
                "op": "play",
                "guildId": self.guild_id,
                "track": track.encoded,
            }
        )

    async def stop(self) -> None:
        self.current = None
        await self.node.send({"op": "stop", "guildId": self.guild_id})

    async def pause(self, pause: bool = True) -> None:
        self.paused = pause
        await self.node.send(
            {"op": "pause", "guildId": self.guild_id, "pause": pause}
        )

    async def set_volume(self, volume: int) -> None:
        self.volume = max(0, min(1000, volume))
        await self.node.send(
            {"op": "volume", "guildId": self.guild_id, "volume": self.volume}
        )

    async def skip(self) -> None:
        if self.queue.is_empty():
            await self.stop()
            return

        next_track = self.queue.pop()
        await self.play(next_track)

    async def shuffle(self) -> None:
        self.queue.shuffle()

    async def _voice_event(self, data: dict[str, object]) -> None:
        await self.node.send(
            {
                "op": "voiceUpdate",
                "guildId": self.guild_id,
                **data,
            }
        )
