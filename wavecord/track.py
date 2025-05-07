from __future__ import annotations

from typing import Optional, Dict, Any


class Track:
    """Represents a single track received from Lavalink."""

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
        self.description: Optional[str] = info.get("description")  # Plugins (e.g. Spotify) might provide this

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"

    def _guess_thumbnail(self) -> Optional[str]:
        """Attempts to generate a thumbnail URL based on the track source."""
        identifier = self.info.get("identifier")
        if self.source.lower() == "youtube" and identifier:
            return f"https://img.youtube.com/vi/{identifier}/hqdefault.jpg"
        return None

    @classmethod
    def build(cls, data: Dict[str, Any]) -> Track:
        """Creates a Track object from Lavalink track data."""
        return cls(encoded=data["track"], info=data["info"])
