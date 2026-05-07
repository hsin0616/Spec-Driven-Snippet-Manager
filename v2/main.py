from __future__ import annotations

import argparse
import sys
from pathlib import Path

from service import (
    add_snippet,
    delete_snippet,
    filter_snippets,
    list_snippets,
    list_starred_snippets,
    search_snippets,
    show_snippet,
    star_snippet,
    update_snippet,
)
from storage import StorageError

SUPPORTED_LIST_SORTS = ("created", "updated")
SUPPORTED_SEARCH_SORTS = ("relevance",)



def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser for v2."""
    parser = argparse.ArgumentParser(description="Knowledge Snippet Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new snippet")
    add_parser.add_argument("--title", required=True, help="Snippet title")
    add_parser.add_argument("--content", required=True, help="Snippet content")
    add_parser.add_argument(
        "--tags",
        required=True,
        help="Comma-separated tags, e.g. programming,python",
    )

    list_parser = subparsers.add_parser("list", help="List all snippets")
    list_parser.add_argument(
        "--sort",
        choices=SUPPORTED_LIST_SORTS,
        help="Sort by created (default behavior) or updated",
    )

    show_parser = subparsers.add_parser("show", help="Show one snippet by ID")
    show_parser.add_argument("--id", type=int, required=True, help="Snippet ID")

    search_parser = subparsers.add_parser(
        "search",
        help="Search snippets by keyword in title or content",
    )
    search_parser.add_argument("--query", required=True, help="Search keyword")
    search_parser.add_argument(
        "--sort",
        choices=SUPPORTED_SEARCH_SORTS,
        help="Sort search results by relevance",
    )

    filter_parser = subparsers.add_parser("filter", help="Filter snippets by tag")
    filter_parser.add_argument("--tag", required=True, help="Tag name")

    delete_parser = subparsers.add_parser("delete", help="Delete one snippet by ID")
    delete_parser.add_argument("--id", type=int, required=True, help="Snippet ID")

    update_parser = subparsers.add_parser("update", help="Update an existing snippet")
    update_parser.add_argument("--id", type=int, required=True, help="Snippet ID")
    update_parser.add_argument("--title", help="New snippet title")
    update_parser.add_argument("--content", help="New snippet content")
    update_parser.add_argument(
        "--tags",
        help="New comma-separated tags, e.g. programming,python",
    )

    star_parser = subparsers.add_parser("star", help="Toggle star for one snippet by ID")
    star_parser.add_argument("--id", type=int, required=True, help="Snippet ID")

    subparsers.add_parser("starred", help="List all starred snippets")

    return parser



def get_storage_path() -> str:
    """Return the default JSON storage path."""
    base_dir = Path(__file__).resolve().parent
    return str(base_dir / "data" / "snippets.json")



def main() -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()
    storage_path = get_storage_path()

    try:
        if args.command == "add":
            print(add_snippet(storage_path, args.title, args.content, args.tags))
            return 0

        if args.command == "list":
            print(list_snippets(storage_path, sort_by=args.sort))
            return 0

        if args.command == "show":
            print(show_snippet(storage_path, args.id))
            return 0

        if args.command == "search":
            print(search_snippets(storage_path, args.query, sort_by=args.sort))
            return 0

        if args.command == "filter":
            print(filter_snippets(storage_path, args.tag))
            return 0

        if args.command == "delete":
            print(delete_snippet(storage_path, args.id))
            return 0

        if args.command == "update":
            print(
                update_snippet(
                    storage_path,
                    args.id,
                    title=args.title,
                    content=args.content,
                    tags_str=args.tags,
                )
            )
            return 0

        if args.command == "star":
            print(star_snippet(storage_path, args.id))
            return 0

        if args.command == "starred":
            print(list_starred_snippets(storage_path))
            return 0

        parser.print_help()
        return 2
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except StorageError as exc:
        print(str(exc), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
