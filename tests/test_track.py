from wavecord.track import Track


def test_track_build_and_attributes():
    data = {
        "track": "abc123",
        "info": {
            "title": "Test Song",
            "author": "Test Artist",
            "length": 300000,
            "isStream": False,
            "uri": "https://example.com",
            "sourceName": "youtube",
            "identifier": "dQw4w9WgXcQ",
        },
    }

    track = Track.build(data)

    assert track.encoded == "abc123"
    assert track.title == "Test Song"
    assert track.author == "Test Artist"
    assert track.duration == 300000
    assert not track.stream
    assert track.uri == "https://example.com"
    assert track.source == "youtube"
    assert track.thumbnail == "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
