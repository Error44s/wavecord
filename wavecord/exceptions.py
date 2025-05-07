class WavecordException(Exception):
    pass


class NodeConnectionError(WavecordException):
    pass


class NodeNotConnected(WavecordException):
    pass


class PlayerNotConnected(WavecordException):
    pass


class TrackLoadError(WavecordException):
    pass


class InvalidTrackType(WavecordException):
    pass
