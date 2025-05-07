from __future__ import annotations

from typing import Any, Dict, Optional


class Track:
    def __init__(self, encoded: str, info: Dict[str, Any]) -> None:
        self.encoded: str = encoded
        self.info: Dict[str, Any] = info

        self.title: str = info.get("title", "Unknown Title")
        self.author: str = info.get("author", "Unknown Author")
        self.duration: int = info.get("length", 0)
        self.stream: bool = info.get("isStream", False)
        self.uri: Optional[str] = info.get("uri")
        self.source: str = info.get("sourceName", "Unknown")
        self.thumbnail: Optional[str] = info.get("artworkUrl") or self._guess_thumbnail()
        self.description: Optional[str] = info.get("description")

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    def _guess_thumbnail(self) -> Optional[str]:
        identifier = self.info.get("identifier")
        if self.source.lower() == "youtube" and identifier:
            return f"https://img.youtube.com/vi/{identifier}/hqdefault.jpg"
        return None

    @classmethod
    def build(cls, data: Dict[str, Any]) -> Track:
        return cls(encoded=data["track"], info=data["info"])
