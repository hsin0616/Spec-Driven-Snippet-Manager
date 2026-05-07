from __future__ import annotations

from typing import Any

from models import Snippet
from storage import get_next_id, load_snippets, save_snippets
from utils import (
    compute_relevance_score,
    ensure_metadata,
    format_added_message,
    format_deleted_message,
    format_snippet_detail,
    format_snippet_summary,
    format_snippet_summary_with_star,
    format_star_message,
    format_updated_message,
    get_timestamp,
    is_starred,
    parse_tags,
)



def add_snippet(storage_path: str, title: str, content: str, tags_str: str) -> str:
    """Add a new snippet and save it to storage."""
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



def list_snippets(storage_path: str, sort_by: str | None = None) -> str:
    """
    List all snippets.

    - None or 'created': preserve v1 insertion order
    - 'updated': latest updated snippet first
    - list output may include a star marker for starred items
    """
    snippets = load_snippets(storage_path)
    if not snippets:
        return "No snippets found"

    ordered_snippets = list(snippets)
    if sort_by == "updated":
        ordered_snippets.sort(
            key=lambda snippet: str(snippet.get("updated_at", "")),
            reverse=True,
        )

    lines = [format_snippet_summary_with_star(snippet) for snippet in ordered_snippets]
    return "\n".join(lines)



def show_snippet(storage_path: str, snippet_id: int) -> str:
    """Show one snippet in full detail format."""
    snippets = load_snippets(storage_path)
    for snippet in snippets:
        if snippet.get("id") == snippet_id:
            return format_snippet_detail(snippet)
    raise ValueError("Error: snippet not found")



def search_snippets(storage_path: str, query: str, sort_by: str | None = None) -> str:
    """
    Search snippets by case-insensitive substring match on title and content.

    - None: preserve v1 insertion order
    - 'relevance': sort by explainable relevance score, highest first
    - output remains the v1 summary format
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

    if sort_by == "relevance":
        matches = sorted(
            matches,
            key=lambda snippet: compute_relevance_score(snippet, normalized_query),
            reverse=True,
        )

    lines = [format_snippet_summary(snippet) for snippet in matches]
    return "\n".join(lines)



def filter_snippets(storage_path: str, tag: str) -> str:
    """
    Filter snippets by case-insensitive tag match.

    Output remains the v1 summary format.
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
    """Delete one snippet by ID and save the updated storage."""
    snippets = load_snippets(storage_path)
    for index, snippet in enumerate(snippets):
        if snippet.get("id") == snippet_id:
            deleted_snippet = snippets.pop(index)
            save_snippets(storage_path, snippets)
            return format_deleted_message(deleted_snippet)
    raise ValueError("Error: snippet not found")



def update_snippet(
    storage_path: str,
    snippet_id: int,
    title: str | None = None,
    content: str | None = None,
    tags_str: str | None = None,
) -> str:
    """Update selected fields of one snippet."""
    if title is None and content is None and tags_str is None:
        raise ValueError("Error: at least one field to update must be provided")

    snippets = load_snippets(storage_path)

    for snippet in snippets:
        if snippet.get("id") != snippet_id:
            continue

        if title is not None:
            snippet["title"] = title
        if content is not None:
            snippet["content"] = content
        if tags_str is not None:
            snippet["tags"] = parse_tags(tags_str)

        snippet["updated_at"] = get_timestamp()
        ensure_metadata(snippet)
        save_snippets(storage_path, snippets)
        return format_updated_message(snippet)

    raise ValueError("Error: snippet not found")



def star_snippet(storage_path: str, snippet_id: int) -> str:
    """Toggle the starred state of one snippet."""
    snippets = load_snippets(storage_path)

    for snippet in snippets:
        if snippet.get("id") != snippet_id:
            continue

        metadata = ensure_metadata(snippet)
        metadata["starred"] = not is_starred(snippet)
        save_snippets(storage_path, snippets)
        return format_star_message(snippet)

    raise ValueError("Error: snippet not found")



def list_starred_snippets(storage_path: str) -> str:
    """List only starred snippets using the same format as list."""
    snippets = load_snippets(storage_path)
    matches = [snippet for snippet in snippets if is_starred(snippet)]

    if not matches:
        return "No snippets found"

    lines = [format_snippet_summary_with_star(snippet) for snippet in matches]
    return "\n".join(lines)
