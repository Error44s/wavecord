from wavecord.exceptions import (
    WavecordException,
    NodeConnectionError,
    NodeNotConnected,
    PlayerNotConnected,
    TrackLoadError,
    InvalidTrackType,
)


def test_exceptions_inheritance_and_str():
    assert isinstance(NodeConnectionError("err"), WavecordException)
    assert isinstance(NodeNotConnected("err"), WavecordException)
    assert isinstance(PlayerNotConnected("err"), WavecordException)
    assert isinstance(TrackLoadError("err"), WavecordException)
    assert isinstance(InvalidTrackType("err"), WavecordException)

    # Optional string checks
    assert str(NodeConnectionError("test")) == "test"
    assert str(InvalidTrackType("invalid")) == "invalid"
