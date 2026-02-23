---
title: "Lab 10.2: Quality Pipeline"
sidebar:
  order: 2
---

This lab is a guided walkthrough — no scaffold file to download. Follow the steps to set up a complete code quality pipeline using black, ruff, mypy, and pytest.

## Goal

Configure four quality tools for a Python project, understand what each one does, and set them up to work together via a single command.

## Step 1: Install the Tools

```bash
pip install black ruff mypy pytest
```

| Tool | What It Does |
|------|-------------|
| **black** | Code formatter — enforces consistent style automatically |
| **ruff** | Linter — catches bugs, style issues, and complexity problems |
| **mypy** | Type checker — validates type annotations |
| **pytest** | Test runner — runs your test suite |

## Step 2: Create a Sample Project

Create a file called `task_manager.py` with some intentional issues:

```python
import os, sys
from typing import List,Optional

class TaskManager:
    def __init__(self):
        self.tasks:list[dict] = []
        self._next_id:int = 1

    def add( self,title:str,priority:int=1 )->dict:
        task = {"id":self._next_id,"title":title,"priority":priority,"done":False}
        self.tasks.append(task)
        self._next_id+=1
        return task

    def complete(self, task_id:int)->None:
        for task in self.tasks:
            if task["id"]==task_id:
                task["done"]=True
                return
        raise KeyError(f"Task {task_id} not found")

    def pending(self)->list[dict]:
        return sorted([t for t in self.tasks if not t["done"]],key=lambda t:t["priority"],reverse=True)

    def remove(self,task_id):
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
```

## Step 3: Run Black (Formatter)

```bash
# Preview changes without applying
black --check --diff task_manager.py

# Apply formatting
black task_manager.py
```

Notice how black:
- Adds consistent spacing around operators and after commas
- Formats long lines to fit within 88 characters
- Standardizes quote style

## Step 4: Run Ruff (Linter)

```bash
ruff check task_manager.py
```

Ruff will flag issues like:
- `F401`: unused imports (`os`, `sys`)
- `UP006`: use `list` instead of `List` (Python 3.9+)

Fix the issues manually or let ruff auto-fix:

```bash
ruff check --fix task_manager.py
```

## Step 5: Run Mypy (Type Checker)

```bash
mypy task_manager.py
```

Mypy will report:
- Missing return type annotations (the `remove` method)
- Any type inconsistencies

Fix by adding type annotations to `remove`:

```python
def remove(self, task_id: int) -> None:
```

## Step 6: Write Tests and Run Pytest

Create `test_task_manager.py`:

```python
import pytest
from task_manager import TaskManager


@pytest.fixture
def manager():
    return TaskManager()


def test_add_task(manager):
    task = manager.add("Write tests")
    assert task["title"] == "Write tests"
    assert task["done"] is False


def test_complete_task(manager):
    task = manager.add("Test task")
    manager.complete(task["id"])
    assert manager.tasks[0]["done"] is True


def test_complete_missing(manager):
    with pytest.raises(KeyError):
        manager.complete(999)


def test_pending_sorted(manager):
    manager.add("Low", priority=1)
    manager.add("High", priority=3)
    manager.add("Medium", priority=2)
    pending = manager.pending()
    assert pending[0]["priority"] == 3
    assert pending[-1]["priority"] == 1
```

Run:

```bash
pytest test_task_manager.py -v
```

## Step 7: Configure `pyproject.toml`

Add tool configuration to a `pyproject.toml` so all tools share settings:

```toml
[tool.black]
line-length = 88

[tool.ruff]
line-length = 88
select = ["E", "F", "UP", "B", "SIM", "I"]

[tool.mypy]
strict = false
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["."]
```

## Step 8: Create a Quality Check Script

Create `check.sh` to run everything in sequence:

```bash
#!/bin/bash
set -e
echo "=== Black (formatting) ==="
black --check .
echo "=== Ruff (linting) ==="
ruff check .
echo "=== Mypy (type checking) ==="
mypy task_manager.py
echo "=== Pytest (tests) ==="
pytest -v
echo "=== All checks passed! ==="
```

```bash
chmod +x check.sh
./check.sh
```

## Checklist

- [ ] Install black, ruff, mypy, and pytest
- [ ] Run black and understand its formatting choices
- [ ] Run ruff and fix all linting warnings
- [ ] Run mypy and add missing type annotations
- [ ] Write at least 4 tests and run them with pytest
- [ ] Create a `pyproject.toml` with tool configuration
- [ ] Create a `check.sh` that runs all tools in sequence
