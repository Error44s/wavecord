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
        """Add a single track to the queue."""
        self._queue.append(track)

    def add_many(self, tracks: List[Track]) -> None:
        """Add multiple tracks to the queue."""
        self._queue.extend(tracks)

    def pop(self) -> Optional[Track]:
        """Remove and return the next track."""
        return self._queue.popleft() if self._queue else None

    def peek(self) -> Optional[Track]:
        """Return the next track without removing it."""
        return self._queue[0] if self._queue else None

    def shuffle(self) -> None:
        """Shuffle the queue."""
        temp = list(self._queue)
        random.shuffle(temp)
        self._queue = deque(temp)

    def clear(self) -> None:
        """Clear the queue."""
        self._queue.clear()

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        return not self._queue

    def to_list(self) -> List[Track]:
        """Return the queue as a list."""
        return list(self._queue)

    def __len__(self) -> int:
        return len(self._queue)

    def __iter__(self) -> Iterator[Track]:
        return iter(self._queue)
