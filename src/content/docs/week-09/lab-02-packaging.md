---
title: "Lab 9.2: Package Publishing"
sidebar:
  order: 2
---

This lab is a guided walkthrough — no scaffold file to download. Follow the steps below to turn your notes app into a proper installable Python package.

## Goal

Create a `pyproject.toml`, restructure your code into a package, and install it in development mode so you can run `notes` from anywhere on your system.

## Step 1: Create the Package Structure

Reorganize your Lab 9.1 code into this structure:

```
notes-app/
├── pyproject.toml
├── README.md
└── src/
    └── notes/
        ├── __init__.py
        ├── cli.py          # argparse logic from main() and build_parser()
        ├── storage.py       # load_notes(), save_notes()
        └── models.py        # add_note(), list_notes(), search_notes(), delete_note()
```

### `__init__.py`

```python
"""Notes — a simple CLI note-taking app."""

__version__ = "0.1.0"
```

### Moving Code

1. **`storage.py`** — Move `load_notes()` and `save_notes()` here. The `NOTES_FILE` path constant goes here too.
2. **`models.py`** — Move `add_note()`, `list_notes()`, `search_notes()`, and `delete_note()` here. Import `load_notes` and `save_notes` from `.storage`.
3. **`cli.py`** — Move `build_parser()` and `main()` here. Import the model functions from `.models`.

## Step 2: Write `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "notes-app"
version = "0.1.0"
description = "A simple CLI note-taking app"
requires-python = ">=3.10"

[project.scripts]
notes = "notes.cli:main"
```

Key sections:
- **`[build-system]`** — Tells pip how to build your package
- **`[project]`** — Package metadata
- **`[project.scripts]`** — Creates a `notes` command that calls `notes.cli:main`

## Step 3: Install in Development Mode

From the `notes-app/` directory:

```bash
pip install -e .
```

The `-e` flag means "editable" — Python links to your source code instead of copying it. Changes you make take effect immediately without reinstalling.

## Step 4: Verify It Works

```bash
# These should all work from any directory
notes add "Test Note" "This is a test" --tags test
notes list
notes search "test"
notes delete 1
```

## Step 5: Add Dependencies (Stretch)

If you want to add color output, add a dependency:

```toml
[project]
# ... existing fields ...
dependencies = [
    "rich>=13.0",
]
```

Then update `cli.py` to use `from rich import print` for colored output. Reinstall with `pip install -e .` to pick up the new dependency.

## Checklist

- [ ] Create the package directory structure under `src/notes/`
- [ ] Split your Lab 9.1 code across `storage.py`, `models.py`, and `cli.py`
- [ ] Write a valid `pyproject.toml` with `[project.scripts]`
- [ ] Install in dev mode with `pip install -e .`
- [ ] Verify the `notes` command works from any directory
- [ ] (Stretch) Add `rich` as a dependency for colored output
