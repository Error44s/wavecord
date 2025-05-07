from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Optional

import aiohttp

from .exceptions import NodeConnectionError
from .events import EventEmitter

if TYPE_CHECKING:
    from .player import WavePlayer


log = logging.getLogger(__name__)


class Node:
    def __init__(
        self,
        host: str,
        port: int = 2333,
        password: str = "youshallnotpass",
        secure: bool = False,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.password = password
        self.secure = secure
        self.session = session or aiohttp.ClientSession()

        self.players: dict[int, WavePlayer] = {}
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.connected = False

        self.events = EventEmitter()

    @property
    def base_url(self) -> str:
        scheme = "https" if self.secure else "http"
        return f"{scheme}://{self.host}:{self.port}"

    async def connect(self) -> None:
        headers = {"Authorization": self.password, "User-Agent": "Wavecord/1.0"}
        ws_url = self.base_url.replace("http", "ws") + "/v4/websocket"

        try:
            self.ws = await self.session.ws_connect(ws_url, headers=headers)
            self.connected = True
            log.info("Connected to Lavalink node at %s", ws_url)

            asyncio.create_task(self.listen())
        except Exception as e:
            log.error("Failed to connect to Lavalink node: %s", e)
            raise NodeConnectionError(f"Could not connect to Lavalink node at {ws_url}") from e

    async def disconnect(self) -> None:
        if self.ws:
            await self.ws.close()
            self.connected = False
            log.info("Disconnected from Lavalink node")

    async def listen(self) -> None:
        if not self.ws:
            return

        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await self.events.emit_raw(msg.data)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                log.warning("WebSocket connection closed")
                self.connected = False
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                log.error("WebSocket error occurred: %s", msg)
                self.connected = False
                break

    async def send(self, data: dict) -> None:
        if not self.ws or self.ws.closed:
            raise NodeConnectionError("WebSocket is not connected")

        await self.ws.send_json(data)