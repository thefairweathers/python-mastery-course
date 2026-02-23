"""
Lab 9.1: CLI Notes App
======================

Build a complete CLI note-taking application with proper module structure.
This single-file version practices the concepts; the stretch goal is to
refactor it into a proper package (see Lab 9.2).

Features:
- Add, list, search, and delete notes
- Notes are stored as JSON in a file
- Command-line interface using argparse
"""

import argparse
import json
from pathlib import Path
from datetime import datetime


NOTES_FILE = Path("notes.json")


def load_notes() -> list[dict]:
    """
    Load notes from the JSON file.

    Return an empty list if the file doesn't exist or is empty.
    Each note is a dict with: id, title, body, created_at, tags
    """
    # TODO: Implement
    pass


def save_notes(notes: list[dict]) -> None:
    """
    Save notes to the JSON file.

    Write with indent=2 for readability.
    """
    # TODO: Implement
    pass


def add_note(title: str, body: str, tags: list[str] | None = None) -> dict:
    """
    Create a new note and save it.

    - Generate an id (max existing id + 1, or 1 if no notes)
    - Set created_at to the current ISO format datetime
    - tags defaults to an empty list

    Return the created note dict.
    """
    # TODO: Implement
    pass


def list_notes(tag: str | None = None) -> list[dict]:
    """
    Return all notes, optionally filtered by tag.

    If tag is provided, return only notes where tag is in the note's tags list.
    """
    # TODO: Implement
    pass


def search_notes(query: str) -> list[dict]:
    """
    Search notes by title and body (case-insensitive).

    Return notes where the query appears in either the title or body.
    """
    # TODO: Implement
    pass


def delete_note(note_id: int) -> bool:
    """
    Delete a note by its id.

    Return True if the note was found and deleted, False otherwise.
    """
    # TODO: Implement
    pass


def build_parser() -> argparse.ArgumentParser:
    """
    Build the argument parser with subcommands:

    notes add "Title" "Body" --tags tag1 tag2
    notes list [--tag TAG]
    notes search QUERY
    notes delete ID
    """
    parser = argparse.ArgumentParser(description="CLI Notes App")
    subparsers = parser.add_subparsers(dest="command")

    # TODO: Add subcommands: add, list, search, delete
    # Hint: Use subparsers.add_parser() for each command

    return parser


def main():
    """Parse arguments and dispatch to the correct function."""
    parser = build_parser()
    args = parser.parse_args()

    # TODO: Dispatch based on args.command
    # - "add": call add_note, print confirmation
    # - "list": call list_notes, print each note
    # - "search": call search_notes, print results
    # - "delete": call delete_note, print success/failure
    # - None: print help

    if args.command is None:
        parser.print_help()


# ============================================================
# Tests — run this file directly to test
# ============================================================

def test_notes():
    # Use a temporary file
    global NOTES_FILE
    original = NOTES_FILE
    NOTES_FILE = Path("/tmp/test_notes.json")
    if NOTES_FILE.exists():
        NOTES_FILE.unlink()

    try:
        # Add notes
        n1 = add_note("Shopping", "Buy milk and eggs", tags=["personal"])
        assert n1["id"] == 1
        assert n1["title"] == "Shopping"
        print("✓ add_note works")

        n2 = add_note("Python Lab", "Finish week 9 labs", tags=["school", "python"])
        assert n2["id"] == 2
        print("✓ auto-increment id works")

        # List
        all_notes = list_notes()
        assert len(all_notes) == 2
        print("✓ list_notes works")

        # Filter by tag
        python_notes = list_notes(tag="python")
        assert len(python_notes) == 1
        assert python_notes[0]["title"] == "Python Lab"
        print("✓ list_notes with tag filter works")

        # Search
        results = search_notes("milk")
        assert len(results) == 1
        print("✓ search_notes works")

        # Delete
        assert delete_note(1) is True
        assert delete_note(999) is False
        assert len(list_notes()) == 1
        print("✓ delete_note works")

    finally:
        NOTES_FILE = original
        Path("/tmp/test_notes.json").unlink(missing_ok=True)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] != "test":
        main()
    else:
        test_notes()
        print("\nAll tests passed! ✓")
