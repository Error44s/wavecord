from typing import TYPE_CHECKING

from discord.ext.commands import AutoShardedBot, Bot

from .exceptions import WavecordException
from .node import Node
from .player import WavePlayer

if TYPE_CHECKING:
    from discord import VoiceChannel


class WaveClient:
    _bot: Bot | AutoShardedBot
    _node: Node
    _players: dict[int, WavePlayer] = {}

    @classmethod
    async def initialize(cls, bot: Bot | AutoShardedBot, node: Node) -> None:
        cls._bot = bot
        cls._node = node
        await node.connect()

        bot._connection.dispatch_lavalink_event = cls._dispatch

    @classmethod
    def get_player(cls, guild_id: int) -> WavePlayer:
        if guild_id not in cls._players:
            cls._players[guild_id] = WavePlayer(guild_id=guild_id, node=cls._node)
        return cls._players[guild_id]

    @classmethod
    async def _dispatch(cls, guild_id: int, payload: dict[str, object]) -> None:
        player = cls._players.get(guild_id)
        if player:
            await player._voice_event(payload)

    @classmethod
    def get_node(cls) -> Node:
        if not hasattr(cls, "_node"):
            raise WavecordException("WaveClient is not initialized.")
        return cls._node
