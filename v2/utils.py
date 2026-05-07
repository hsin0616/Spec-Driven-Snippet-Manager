from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def parse_tags(tags_str: str) -> list[str]:
    """
    Parse a comma-separated tag string into a normalized list of tags.

    Rules:
    - split by comma
    - trim leading/trailing whitespace
    - convert to lowercase
    - ignore empty tags
    - remove duplicates while preserving order
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
    """Return the current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")



def ensure_metadata(snippet: dict[str, Any]) -> dict[str, Any]:
    """Ensure the snippet has a mutable metadata dictionary."""
    metadata = snippet.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
        snippet["metadata"] = metadata
    return metadata



def is_starred(snippet: dict[str, Any]) -> bool:
    """Return True if the snippet is starred, otherwise False."""
    metadata = snippet.get("metadata")
    if not isinstance(metadata, dict):
        return False
    return bool(metadata.get("starred", False))



def format_snippet_summary(snippet: dict[str, Any]) -> str:
    """
    Format one snippet as the v1 stable one-line summary.

    Expected format:
        [1] Python | Tags: programming, python
    """
    snippet_id = snippet["id"]
    title = snippet["title"]
    tags = snippet.get("tags", [])
    tags_str = ", ".join(tags)
    return f"[{snippet_id}] {title} | Tags: {tags_str}"



def format_snippet_summary_with_star(snippet: dict[str, Any]) -> str:
    """
    Format one snippet as a list/starred summary.

    Starred items append a minimal visual marker to satisfy v2.
    """
    snippet_id = snippet["id"]
    title = snippet["title"]
    if is_starred(snippet):
        title = f"{title} ★"
    tags = snippet.get("tags", [])
    tags_str = ", ".join(tags)
    return f"[{snippet_id}] {title} | Tags: {tags_str}"



def format_snippet_detail(snippet: dict[str, Any]) -> str:
    """
    Format one snippet as a full detail block.

    Output remains identical to v1 to preserve backward compatibility.
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



def format_added_message(snippet: dict[str, Any]) -> str:
    """Format the stable success message for add."""
    return f"Added: [{snippet['id']}] {snippet['title']}"



def format_deleted_message(snippet: dict[str, Any]) -> str:
    """Format the stable success message for delete."""
    return f"Deleted: [{snippet['id']}] {snippet['title']}"



def format_updated_message(snippet: dict[str, Any]) -> str:
    """Format the success message for update."""
    return f"Updated: [{snippet['id']}] {snippet['title']}"



def format_star_message(snippet: dict[str, Any]) -> str:
    """Format the success message for star toggle."""
    if is_starred(snippet):
        return f"Starred: [{snippet['id']}] {snippet['title']}"
    return f"Unstarred: [{snippet['id']}] {snippet['title']}"



def compute_relevance_score(snippet: dict[str, Any], query: str) -> int:
    """
    Compute an explainable relevance score.

    Rules:
    - each title occurrence counts as 3
    - each content occurrence counts as 1
    - matching is case-insensitive
    """
    normalized_query = query.strip().lower()
    if not normalized_query:
        return 0

    title = str(snippet.get("title", "")).lower()
    content = str(snippet.get("content", "")).lower()

    title_hits = title.count(normalized_query)
    content_hits = content.count(normalized_query)
    return title_hits * 3 + content_hits
