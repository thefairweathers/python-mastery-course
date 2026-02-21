---
title: "Lab 10.1: Test Suite"
sidebar:
  order: 1
---

> **Download:** [`lab_01_testing.py`](/python-mastery-course/scaffolds/week-10/lab_01_testing.py)

```python
"""
Lab 10.1: Test Suite — Write tests for a TaskManager using pytest.
Run with: pytest lab_01_testing.py -v
"""
import pytest

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self._next_id = 1

    def add(self, title: str, priority: int = 1) -> dict:
        task = {"id": self._next_id, "title": title, "priority": priority, "done": False}
        self.tasks[self._next_id] = task
        self._next_id += 1
        return task

    def complete(self, task_id: int) -> None:
        if task_id not in self.tasks:
            raise KeyError(f"Task {task_id} not found")
        self.tasks[task_id]["done"] = True

    def pending(self) -> list[dict]:
        return sorted(
            [t for t in self.tasks.values() if not t["done"]],
            key=lambda t: t["priority"], reverse=True
        )

# TODO: Write tests for TaskManager
# - test_add_task: adding a task returns a dict with correct title
# - test_complete_task: completing a task sets done=True
# - test_complete_missing: completing non-existent task raises KeyError
# - test_pending_sorted: pending tasks are sorted by priority (highest first)
# - test_pending_excludes_done: completed tasks don't appear in pending

@pytest.fixture
def manager():
    """Provide a fresh TaskManager for each test."""
    return TaskManager()

def test_add_task(manager):
    # TODO
    pass

def test_complete_missing(manager):
    # TODO: Use pytest.raises
    pass
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
