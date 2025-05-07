from __future__ import annotations

import random
from collections import deque
from typing import Deque, Iterator, List, Optional

from .track import Track


class TrackQueue:
    """A simple FIFO queue that manages upcoming tracks."""

    def __init__(self) -> None:
        self._queue: Deque[Track] = deque()

    def add(self, track: Track) -> None:
        self._queue.append(track)

    def add_many(self, tracks: List[Track]) -> None:
        self._queue.extend(tracks)

    def pop(self) -> Optional[Track]:
        return self._queue.popleft() if self._queue else None

    def peek(self) -> Optional[Track]:
        return self._queue[0] if self._queue else None

    def shuffle(self) -> None:
        temp = list(self._queue)
        random.shuffle(temp)
        self._queue = deque(temp)

    def clear(self) -> None:
        self._queue.clear()

    def is_empty(self) -> bool:
        return not self._queue

    def to_list(self) -> List[Track]:
        return list(self._queue)

    def __len__(self) -> int:
        return len(self._queue)

    def __iter__(self) -> Iterator[Track]:
        return iter(self._queue)
