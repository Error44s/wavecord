from __future__ import annotations
from typing import Callable, DefaultDict, List, Any
from collections import defaultdict
import inspect


class EventEmitter:
    """A minimal async event emitter system for internal hooks."""

    def __init__(self):
        self._listeners: DefaultDict[str, List[Callable[..., Any]]] = defaultdict(list)

    def on(self, event: str, callback: Callable[..., Any]) -> None:
        """Registers a new listener for an event."""
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable[..., Any]) -> None:
        """Removes a listener from an event."""
        if callback in self._listeners[event]:
            self._listeners[event].remove(callback)

    async def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Emits an event to all registered listeners."""
        for callback in self._listeners.get(event, []):
            if inspect.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)


# Global emitter instance
emitter = EventEmitter()
