from __future__ import annotations

from typing import Any

from models import Snippet
from storage import get_next_id, load_snippets, save_snippets
from utils import (
    format_added_message,
    format_deleted_message,
    format_snippet_detail,
    format_snippet_summary,
    get_timestamp,
    parse_tags,
)


def add_snippet(storage_path: str, title: str, content: str, tags_str: str) -> str:
    """
    Add a new snippet and save it to storage.

    Returns:
        Stable success message, e.g.:
        Added: [1] Python
    """
    snippets = load_snippets(storage_path)
    next_id = get_next_id(snippets)
    timestamp = get_timestamp()
    tags = parse_tags(tags_str)

    snippet = Snippet(
        id=next_id,
        title=title,
        content=content,
        tags=tags,
        created_at=timestamp,
        updated_at=timestamp,
        metadata={},
    )

    snippets.append(snippet.to_dict())
    save_snippets(storage_path, snippets)

    return format_added_message(snippet.to_dict())


def list_snippets(storage_path: str) -> str:
    """
    List all snippets in stable one-line summary format.

    Returns:
        - 'No snippets found' if empty
        - one summary line per snippet otherwise
    """
    snippets = load_snippets(storage_path)

    if not snippets:
        return "No snippets found"

    lines = [format_snippet_summary(snippet) for snippet in snippets]
    return "\n".join(lines)


def show_snippet(storage_path: str, snippet_id: int) -> str:
    """
    Show one snippet in full detail format.

    Raises:
        ValueError: if snippet is not found
    """
    snippets = load_snippets(storage_path)

    for snippet in snippets:
        if snippet.get("id") == snippet_id:
            return format_snippet_detail(snippet)

    raise ValueError("Error: snippet not found")


def search_snippets(storage_path: str, query: str) -> str:
    """
    Search snippets by case-insensitive substring match
    on title and content only.

    Returns:
        - 'No matching snippets found' if no matches
        - one summary line per matching snippet otherwise
    """
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Error: query must not be empty")

    snippets = load_snippets(storage_path)
    normalized_query = query.strip().lower()

    matches: list[dict[str, Any]] = []
    for snippet in snippets:
        title = str(snippet.get("title", "")).lower()
        content = str(snippet.get("content", "")).lower()

        if normalized_query in title or normalized_query in content:
            matches.append(snippet)

    if not matches:
        return "No matching snippets found"

    lines = [format_snippet_summary(snippet) for snippet in matches]
    return "\n".join(lines)


def filter_snippets(storage_path: str, tag: str) -> str:
    """
    Filter snippets by case-insensitive tag match.

    Returns:
        - 'No matching snippets found' if no matches
        - one summary line per matching snippet otherwise
    """
    if not isinstance(tag, str) or not tag.strip():
        raise ValueError("Error: tag must not be empty")

    snippets = load_snippets(storage_path)
    normalized_tag = tag.strip().lower()

    matches: list[dict[str, Any]] = []
    for snippet in snippets:
        tags = snippet.get("tags", [])
        normalized_tags = [str(t).strip().lower() for t in tags]

        if normalized_tag in normalized_tags:
            matches.append(snippet)

    if not matches:
        return "No matching snippets found"

    lines = [format_snippet_summary(snippet) for snippet in matches]
    return "\n".join(lines)


def delete_snippet(storage_path: str, snippet_id: int) -> str:
    """
    Delete one snippet by ID and save the updated storage.

    Returns:
        Stable success message, e.g.:
        Deleted: [1] Python

    Raises:
        ValueError: if snippet is not found
    """
    snippets = load_snippets(storage_path)

    for index, snippet in enumerate(snippets):
        if snippet.get("id") == snippet_id:
            deleted_snippet = snippets.pop(index)
            save_snippets(storage_path, snippets)
            return format_deleted_message(deleted_snippet)

    raise ValueError("Error: snippet not found")
