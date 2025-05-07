class WavecordException(Exception):
    """Base exception for all Wavecord-related errors."""
    pass


class NodeConnectionError(WavecordException):
    """Raised when a connection to the Lavalink node fails."""
    pass


class NodeNotConnected(WavecordException):
    """Raised when attempting to use a node that isn't connected."""
    pass


class PlayerNotConnected(WavecordException):
    """Raised when trying to control a player that hasn't connected to a voice channel."""
    pass


class TrackLoadError(WavecordException):
    """Raised when a track fails to load or is invalid."""
    pass


class InvalidTrackType(WavecordException):
    """Raised when a given object is not a valid Track instance."""
    pass