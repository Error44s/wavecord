from __future__ import annotations

import inspect
from collections import defaultdict
from typing import Any, Callable, DefaultDict

class EventEmitter:
    def __init__(self) -> None:
        self._listeners: DefaultDict[str, list[Callable[..., Any]]] = defaultdict(list)

    def on(self, event: str, callback: Callable[..., Any]) -> None:
        self._listeners[event].append(callback)

    def off(self, event: str, callback: Callable[..., Any]) -> None:
        if callback in self._listeners[event]:
            self._listeners[event].remove(callback)

    async def emit(self, event: str, *args: Any, **kwargs: Any) -> None:
        for callback in self._listeners.get(event, []):
            if inspect.iscoroutinefunction(callback):
                await callback(*args, **kwargs)
            else:
                callback(*args, **kwargs)


emitter = EventEmitter()
