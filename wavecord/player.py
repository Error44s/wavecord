from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from .track import Track
from .queue import Queue
from .exceptions import WavecordException

if TYPE_CHECKING:
    from .node import Node
    from discord import VoiceChannel


class WavePlayer:
    """Manages playback for a guild."""

    def __init__(self, guild_id: int, node: Node):
        self.guild_id = guild_id
        self.node = node
        self.channel_id: Optional[int] = None
        self.queue: Queue = Queue()
        self.volume: int = 100
        self.paused: bool = False
        self.current: Optional[Track] = None

    async def connect(self, channel: VoiceChannel):
        """Connects to a voice channel."""
        self.channel_id = channel.id
        await self.node._send_voice_update(self.guild_id, channel.id)

    async def play(self, track: Track):
        """Plays a specific track."""
        self.current = track
        await self.node._send(
            op="play",
            guildId=self.guild_id,
            track=track.encoded,
        )

    async def stop(self):
        """Stops playback and clears current."""
        self.current = None
        await self.node._send(op="stop", guildId=self.guild_id)

    async def pause(self, pause: bool = True):
        """Pauses or resumes playback."""
        self.paused = pause
        await self.node._send(op="pause", guildId=self.guild_id, pause=pause)

    async def set_volume(self, volume: int):
        """Sets the player volume (0-1000)."""
        self.volume = max(0, min(1000, volume))
        await self.node._send(op="volume", guildId=self.guild_id, volume=self.volume)

    async def skip(self):
        """Skips to the next track in queue."""
        if self.queue.is_empty():
            await self.stop()
            return

        next_track = self.queue.pop()
        await self.play(next_track)

    async def shuffle(self):
        """Shuffles the current queue."""
        self.queue.shuffle()

    async def _voice_event(self, data: dict):
        """Handles internal voice updates."""
        await self.node._voice_state_update(self.guild_id, data)