from __future__ import annotations

import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any


class StorageError(Exception):
    """Raised when snippet storage cannot be loaded or saved safely."""


def load_snippets(path: str) -> list[dict[str, Any]]:
    """
    Load snippets from a JSON file.

    Rules:
    - If the file does not exist, return an empty list.
    - If the file exists but cannot be parsed, raise StorageError.
    - The top-level JSON value must be a list.
    """
    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except JSONDecodeError as exc:
        raise StorageError("Error: failed to load storage") from exc
    except OSError as exc:
        raise StorageError("Error: failed to load storage") from exc

    if not isinstance(data, list):
        raise StorageError("Error: failed to load storage")

    return data


def save_snippets(path: str, snippets: list[dict[str, Any]]) -> None:
    """
    Save snippets to a JSON file.

    Rules:
    - Parent directories are created automatically if needed.
    - Raises StorageError if writing fails.
    """
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(snippets, f, indent=2, ensure_ascii=False)
    except OSError as exc:
        raise StorageError("Error: failed to save storage") from exc


def get_next_id(snippets: list[dict[str, Any]]) -> int:
    """
    Return the next snippet ID.

    Rules:
    - IDs must not be reused.
    - Next ID is max(existing IDs) + 1.
    - If the list is empty, return 1.
    """
    if not snippets:
        return 1

    max_id = 0
    for snippet in snippets:
        snippet_id = snippet.get("id")
        if not isinstance(snippet_id, int):
            raise StorageError("Error: failed to load storage")
        if snippet_id > max_id:
            max_id = snippet_id

    return max_id + 1
