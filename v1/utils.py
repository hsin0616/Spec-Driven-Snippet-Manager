from __future__ import annotations

from datetime import datetime, timezone


def parse_tags(tags_str: str) -> list[str]:
    """
    Parse a comma-separated tag string into a normalized list of tags.

    Rules:
    - split by comma
    - trim leading/trailing whitespace
    - convert to lowercase
    - ignore empty tags
    - remove duplicates while preserving order

    Example:
        " Python, ai ,python,  ,Study "
        -> ["python", "ai", "study"]
    """
    if not isinstance(tags_str, str):
        raise TypeError("tags_str must be a str")

    normalized_tags: list[str] = []
    seen: set[str] = set()

    for raw_tag in tags_str.split(","):
        tag = raw_tag.strip().lower()
        if not tag:
            continue
        if tag not in seen:
            seen.add(tag)
            normalized_tags.append(tag)

    return normalized_tags


def get_timestamp() -> str:
    """
    Return the current UTC timestamp in ISO 8601 format.

    Example:
        "2026-03-15T10:00:00Z"
    """
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def format_snippet_summary(snippet: dict) -> str:
    """
    Format one snippet as a stable one-line summary.

    Expected format:
        [1] Python | Tags: programming, python
    """
    snippet_id = snippet["id"]
    title = snippet["title"]
    tags = snippet.get("tags", [])
    tags_str = ", ".join(tags)
    return f"[{snippet_id}] {title} | Tags: {tags_str}"


def format_snippet_detail(snippet: dict) -> str:
    """
    Format one snippet as a full detail block.

    Expected format:
        ID: 1
        Title: Python
        Content: Decorator
        Tags: programming, python
        Created At: 2026-03-15T10:00:00Z
        Updated At: 2026-03-15T10:00:00Z
    """
    tags = snippet.get("tags", [])
    tags_str = ", ".join(tags)

    lines = [
        f"ID: {snippet['id']}",
        f"Title: {snippet['title']}",
        f"Content: {snippet['content']}",
        f"Tags: {tags_str}",
        f"Created At: {snippet['created_at']}",
        f"Updated At: {snippet['updated_at']}",
    ]
    return "\n".join(lines)


def format_added_message(snippet: dict) -> str:
    """
    Format the stable success message for add.
    """
    return f"Added: [{snippet['id']}] {snippet['title']}"


def format_deleted_message(snippet: dict) -> str:
    """
    Format the stable success message for delete.
    """
    return f"Deleted: [{snippet['id']}] {snippet['title']}"
