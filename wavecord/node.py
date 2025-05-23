from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Optional

import aiohttp

from .events import emitter
from .exceptions import NodeConnectionError, TrackLoadError
from .track import Track

if TYPE_CHECKING:
    from .player import WavePlayer

log = logging.getLogger("wavecord.node")


class Node:
    def __init__(
        self,
        host: str,
        port: int = 2333,
        password: str = "youshallnotpass",
        secure: bool = False,
        user_id: Optional[int] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.password = password
        self.secure = secure
        self.user_id = user_id
        self.session = session or aiohttp.ClientSession()

        self.players: dict[int, WavePlayer] = {}
        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.connected = False

    @property
    def base_url(self) -> str:
        scheme = "https" if self.secure else "http"
        return f"{scheme}://{self.host}:{self.port}"

    async def connect(self) -> None:
        if self.user_id is None:
            raise NodeConnectionError("User ID is required for Lavalink v4")

        headers = {
            "Authorization": self.password,
            "User-Id": str(self.user_id),
            "User-Agent": "Wavecord/1.0",
        }
        ws_url = self.base_url.replace("http", "ws") + "/v4/websocket"

        try:
            self.ws = await self.session.ws_connect(ws_url, headers=headers)
            self.connected = True
            log.info("✅ Connected to Lavalink node at %s", ws_url)
            asyncio.create_task(self.listen())
        except Exception as e:
            log.error("❌ Failed to connect to Lavalink node: %s", e)
            raise NodeConnectionError(
                f"Could not connect to Lavalink node at {ws_url}"
            ) from e

    async def disconnect(self) -> None:
        if self.ws and not self.ws.closed:
            await self.ws.close()
            self.connected = False
            log.info("🔌 Disconnected from Lavalink node")

    async def listen(self) -> None:
        if not self.ws:
            return

        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                await emitter.emit("raw_event", msg.json())
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                log.warning("⚠️ WebSocket connection closed")
                self.connected = False
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                log.error("💥 WebSocket error occurred: %s", msg)
                self.connected = False
                break

    async def send(self, data: dict[str, object]) -> None:
        if not self.ws or self.ws.closed:
            raise NodeConnectionError("WebSocket is not connected")

        await self.ws.send_json(data)

    async def load_tracks(self, identifier: str) -> list[Track]:
        async with self.session.get(
            f"{self.base_url}/v4/loadtracks",
            params={"identifier": identifier},
            headers={"Authorization": self.password},
        ) as resp:
            if resp.status != 200:
                raise TrackLoadError(f"Failed to load tracks for: {identifier}")
    
            data = await resp.json()
            load_type = data.get("loadType")
            track_data = data.get("data") or data.get("tracks")
    
            if load_type in ("NO_MATCHES", "LOAD_FAILED") or not track_data:
                return []
    
            valid_tracks = [
                Track.build(track)
                for track in track_data
                if isinstance(track, dict) and "track" in track and "info" in track
            ]
            return valid_tracks



