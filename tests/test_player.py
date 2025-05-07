import pytest
from wavecord.player import WavePlayer
from wavecord.track import Track
from wavecord.queue import TrackQueue
from wavecord.exceptions import PlayerNotConnected


class DummyNode:
    def __init__(self):
        self.sent_payloads = []

    async def send(self, data: dict) -> None:
        self.sent_payloads.append(data)


@pytest.mark.asyncio
async def test_play_raises_if_not_connected():
    node = DummyNode()
    player = WavePlayer(guild_id=12345, node=node)

    track = Track("abc123", {"title": "Test", "author": "Tester", "length": 1000})

    with pytest.raises(PlayerNotConnected):
        await player.play(track)


@pytest.mark.asyncio
async def test_skip_works_correctly():
    node = DummyNode()
    player = WavePlayer(guild_id=123, node=node)
    player.channel_id = 999  # simulate connected
    track1 = Track("track1", {"title": "T1", "author": "A1", "length": 1234})
    track2 = Track("track2", {"title": "T2", "author": "A2", "length": 5678})

    player.queue.add(track1)
    player.queue.add(track2)
    await player.play(player.queue.pop())  # Play first track

    await player.skip()  # Should play second track

    assert player.current == track2
    assert player.queue.is_empty()
