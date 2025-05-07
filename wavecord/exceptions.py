class WavecordException(Exception):
    """Base exception for all Wavecord-related errors."""
    ...


class NodeConnectionError(WavecordException):
    """Raised when a connection to the Lavalink node fails."""
    ...


class NodeNotConnected(WavecordException):
    """Raised when attempting to use a node that isn't connected."""
    ...


class PlayerNotConnected(WavecordException):
    """Raised when trying to control a player that hasn't connected to a voice channel."""
    ...


class TrackLoadError(WavecordException):
    """Raised when a track fails to load or is invalid."""
    ...


class InvalidTrackType(WavecordException):
    """Raised when a given object is not a valid Track instance."""
    ...
