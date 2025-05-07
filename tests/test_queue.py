import pytest
from wavecord.queue import TrackQueue
from wavecord.track import Track

@pytest.fixture
def dummy_track():
    return Track("abc123", {
        "title": "Test Song",
        "author": "Test Author",
        "length": 123456,
        "isStream": False,
        "uri": "http://test",
        "sourceName": "youtube",
        "identifier": "dQw4w9WgXcQ"
    })

def test_add_and_pop(dummy_track):
    queue = TrackQueue()
    queue.add(dummy_track)
    assert len(queue) == 1
    popped = queue.pop()
    assert popped.title == "Test Song"
    assert queue.is_empty()
