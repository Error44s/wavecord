from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .track import Track
from .queue import Queue
from .exceptions import PlayerNotConnected, WavecordException

if TYPE_CHECKING:
    from .node import Node
    from discord import VoiceChannel


class WavePlayer:
    """Manages playback and queue logic for a guild."""

    def __init__(self, guild_id: int, node: Node) -> None:
        self.guild_id: int = guild_id
        self.node: Node = node
        self.channel_id: Optional[int] = None
        self.queue: Queue = Queue()
        self.volume: int = 100
        self.paused: bool = False
        self.current: Optional[Track] = None

    async def connect(self, channel: VoiceChannel) -> None:
        """Connect the player to a Discord voice channel."""
        self.channel_id = channel.id
        await self.node.send({
            "op": "voiceUpdate",
            "guildId": self.guild_id,
            "channelId": str(channel.id),
        })

    async def play(self, track: Track) -> None:
        """Start playing a track."""
        if not self.channel_id:
            raise PlayerNotConnected("Player is not connected to a voice channel.")

        self.current = track
        await self.node.send({
            "op": "play",
            "guildId": self.guild_id,
            "track": track.encoded,
        })

    async def stop(self) -> None:
        """Stop playback."""
        self.current = None
        await self.node.send({
            "op": "stop",
            "guildId": self.guild_id,
        })

    async def pause(self, pause: bool = True) -> None:
        """Pause or resume playback."""
        self.paused = pause
        await self.node.send({
            "op": "pause",
            "guildId": self.guild_id,
            "pause": pause,
        })

    async def set_volume(self, volume: int) -> None:
        """Set the volume (0–1000)."""
        self.volume = max(0, min(1000, volume))
        await self.node.send({
            "op": "volume",
            "guildId": self.guild_id,
            "volume": self.volume,
        })

    async def skip(self) -> None:
        """Skip the current track and play the next in queue."""
        if self.queue.is_empty():
            await self.stop()
            return

        next_track = self.queue.pop()
        await self.play(next_track)

    async def shuffle(self) -> None:
        """Shuffle the queue."""
        self.queue.shuffle()

    async def _voice_event(self, data: dict) -> None:
        """Handle internal voice state/server updates."""
        await self.node.send({
            "op": "voiceUpdate",
            "guildId": self.guild_id,
            **data,
        })
