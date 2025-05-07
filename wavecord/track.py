from __future__ import annotations
from typing import Optional, Dict


class Track:
    """Represents a Lavalink track."""

    def __init__(self, encoded: str, info: Dict):
        self.encoded = encoded
        self.info = info

        self.title: str = info.get("title", "Unknown Title")
        self.author: str = info.get("author", "Unknown Author")
        self.duration: int = info.get("length", 0)
        self.stream: bool = info.get("isStream", False)
        self.uri: Optional[str] = info.get("uri")
        self.thumbnail: Optional[str] = info.get("artworkUrl") or self._get_thumbnail()
        self.description: Optional[str] = info.get("description")  # if plugins provide it

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    def _get_thumbnail(self) -> Optional[str]:
        # Tries to extract a YouTube thumbnail if available
        identifier = self.info.get("identifier")
        if identifier and "youtube" in self.info.get("sourceName", "").lower():
            return f"https://img.youtube.com/vi/{identifier}/hqdefault.jpg"
        return None

    @classmethod
    def build(cls, data: Dict) -> Track:
        """Builds a Track from Lavalink JSON response."""
        return cls(encoded=data["track"], info=data["info"])