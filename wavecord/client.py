from typing import Optional, TYPE_CHECKING
from discord.ext.commands import Bot, AutoShardedBot
from .node import Node
from .player import WavePlayer
from .exceptions import WavecordException

if TYPE_CHECKING:
    from discord import VoiceChannel, Guild


class WaveClient:
    """Main controller for all Lavalink-related logic."""

    _bot: Bot | AutoShardedBot
    _node: Node
    _players: dict[int, WavePlayer] = {}

    @classmethod
    async def initialize(cls, bot: Bot | AutoShardedBot, node: Node):
        """Initialize Wavecord and connect the node."""
        cls._bot = bot
        cls._node = node
        await node.connect()

        # Attach WebSocket hook
        bot._connection.dispatch_lavalink_event = cls._dispatch

    @classmethod
    def get_player(cls, guild_id: int) -> WavePlayer:
        """Return an existing or new player for a guild."""
        if guild_id not in cls._players:
            cls._players[guild_id] = WavePlayer(guild_id=guild_id, node=cls._node)
        return cls._players[guild_id]

    @classmethod
    async def _dispatch(cls, guild_id: int, payload: dict):
        """Handle raw WebSocket events (voice state/server updates)."""
        player = cls._players.get(guild_id)
        if player:
            await player._voice_event(payload)

    @classmethod
    def get_node(cls) -> Node:
        if not hasattr(cls, "_node"):
            raise WavecordException("WaveClient is not initialized.")
        return cls._node