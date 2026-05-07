from __future__ import annotations

import argparse
import sys
from pathlib import Path

from service import (
    add_snippet,
    delete_snippet,
    filter_snippets,
    list_snippets,
    search_snippets,
    show_snippet,
)
from storage import StorageError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Knowledge Snippet Manager"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a new snippet")
    add_parser.add_argument("--title", required=True, help="Snippet title")
    add_parser.add_argument("--content", required=True, help="Snippet content")
    add_parser.add_argument(
        "--tags",
        required=True,
        help="Comma-separated tags, e.g. programming,python",
    )

    # list
    subparsers.add_parser("list", help="List all snippets")

    # show
    show_parser = subparsers.add_parser("show", help="Show one snippet by ID")
    show_parser.add_argument("--id", type=int, required=True, help="Snippet ID")

    # search
    search_parser = subparsers.add_parser(
        "search",
        help="Search snippets by keyword in title or content",
    )
    search_parser.add_argument(
        "--query",
        required=True,
        help="Search keyword",
    )

    # filter
    filter_parser = subparsers.add_parser(
        "filter",
        help="Filter snippets by tag",
    )
    filter_parser.add_argument(
        "--tag",
        required=True,
        help="Tag name",
    )

    # delete
    delete_parser = subparsers.add_parser("delete", help="Delete one snippet by ID")
    delete_parser.add_argument("--id", type=int, required=True, help="Snippet ID")

    return parser


def get_storage_path() -> str:
    base_dir = Path(__file__).resolve().parent
    return str(base_dir / "data" / "snippets.json")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    storage_path = get_storage_path()

    try:
        if args.command == "add":
            result = add_snippet(
                storage_path=storage_path,
                title=args.title,
                content=args.content,
                tags_str=args.tags,
            )
            print(result)
            return 0

        if args.command == "list":
            result = list_snippets(storage_path=storage_path)
            print(result)
            return 0

        if args.command == "show":
            result = show_snippet(
                storage_path=storage_path,
                snippet_id=args.id,
            )
            print(result)
            return 0

        if args.command == "search":
            result = search_snippets(
                storage_path=storage_path,
                query=args.query,
            )
            print(result)
            return 0

        if args.command == "filter":
            result = filter_snippets(
                storage_path=storage_path,
                tag=args.tag,
            )
            print(result)
            return 0

        if args.command == "delete":
            result = delete_snippet(
                storage_path=storage_path,
                snippet_id=args.id,
            )
            print(result)
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
