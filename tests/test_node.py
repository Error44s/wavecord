import pytest
from wavecord.node import Node
from wavecord.exceptions import NodeConnectionError


class DummyWebSocket:
    closed = False

    async def send_json(self, data):
        self.last_sent = data

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_send_raises_when_not_connected():
    node = Node("localhost")
    node.ws = None  # simulate not connected
    with pytest.raises(NodeConnectionError):
        await node.send({"op": "play"})


@pytest.mark.asyncio
async def test_send_json_successfully():
    node = Node("localhost")
    node.ws = DummyWebSocket()
    await node.send({"op": "ping"})

    assert node.ws.last_sent["op"] == "ping"
