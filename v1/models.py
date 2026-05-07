from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Snippet:
    """
    Core data model for one knowledge snippet.

    Fields follow the v1 SDD:
    - id: unique integer ID
    - title: short title, must be non-empty
    - content: main text, must be non-empty
    - tags: list of normalized tag strings
    - created_at: ISO 8601 timestamp string
    - updated_at: ISO 8601 timestamp string
    - metadata: reserved for future extension
    """

    id: int
    title: str
    content: str
    tags: list[str]
    created_at: str
    updated_at: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._validate()
        self.tags = self._normalize_tags(self.tags)
        if self.metadata is None:
            self.metadata = {}

    def _validate(self) -> None:
        if not isinstance(self.id, int):
            raise TypeError("id must be an int")

        if not isinstance(self.title, str):
            raise TypeError("title must be a str")
        if not self.title.strip():
            raise ValueError("title must not be empty")

        if not isinstance(self.content, str):
            raise TypeError("content must be a str")
        if not self.content.strip():
            raise ValueError("content must not be empty")

        if not isinstance(self.tags, list):
            raise TypeError("tags must be a list[str]")

        if not isinstance(self.created_at, str):
            raise TypeError("created_at must be a str")

        if not isinstance(self.updated_at, str):
            raise TypeError("updated_at must be a str")

        if self.metadata is not None and not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dict")

    @staticmethod
    def _normalize_tags(tags: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()

        for tag in tags:
            if not isinstance(tag, str):
                raise TypeError("each tag must be a str")

            cleaned = tag.strip().lower()
            if not cleaned:
                continue

            if cleaned not in seen:
                seen.add(cleaned)
                normalized.append(cleaned)

        return normalized

    def to_dict(self) -> dict[str, Any]:
        """Convert Snippet to a JSON-serializable dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Snippet":
        """Create a Snippet instance from a dictionary."""
        return cls(
            id=data["id"],
            title=data["title"],
            content=data["content"],
            tags=data["tags"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            metadata=data.get("metadata", {}),
        )
