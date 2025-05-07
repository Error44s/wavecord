from collections import deque
from typing import Deque, Optional, List
from .track import Track
import random


class TrackQueue:
    """A simple FIFO queue to store tracks."""

    def __init__(self) -> None:
        self._queue: Deque[Track] = deque()

    def put(self, track: Track) -> None:
        self._queue.append(track)

    def put_many(self, tracks: List[Track]) -> None:
        self._queue.extend(tracks)

    def get(self) -> Optional[Track]:
        return self._queue.popleft() if self._queue else None

    def peek(self) -> Optional[Track]:
        return self._queue[0] if self._queue else None

    def clear(self) -> None:
        self._queue.clear()

    def shuffle(self) -> None:
        temp = list(self._queue)
        random.shuffle(temp)
        self._queue = deque(temp)

    def __len__(self) -> int:
        return len(self._queue)

    def __iter__(self):
        return iter(self._queue)

    def to_list(self) -> List[Track]:
        return list(self._queue)