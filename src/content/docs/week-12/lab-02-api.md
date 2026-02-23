---
title: "Lab 12.2: REST API"
sidebar:
  order: 2
---

> **Download:** [`lab_02_api.py`](/python-mastery-course/scaffolds/week-12/lab_02_api.py)

```python
"""
Lab 12.2: REST API
==================

Build a task management API with FastAPI.
Practice route handlers, request validation, and HTTP methods.

Install: pip install fastapi uvicorn
Run: uvicorn lab_02_api:app --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Task Manager API")


# ============================================================
# Models
# ============================================================

class TaskCreate(BaseModel):
    """Request body for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    priority: int = Field(default=1, ge=1, le=5)


class TaskUpdate(BaseModel):
    """Request body for updating a task. All fields optional."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    priority: int | None = Field(default=None, ge=1, le=5)
    done: bool | None = None


class TaskResponse(BaseModel):
    """Response body for a task."""
    id: int
    title: str
    description: str
    priority: int
    done: bool


# ============================================================
# In-Memory Storage
# ============================================================

tasks_db: dict[int, dict] = {}
next_id: int = 1


# ============================================================
# Routes — TODO: Implement each endpoint
# ============================================================

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(done: bool | None = None, min_priority: int = 1):
    """
    List all tasks with optional filters.

    Query params:
    - done: filter by completion status (optional)
    - min_priority: only return tasks with priority >= this value (default 1)

    Return the list sorted by priority (highest first).
    """
    # TODO: Implement
    pass


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate):
    """
    Create a new task.

    - Auto-assign an id (use the global next_id counter)
    - Set done=False by default
    - Return the created task with 201 status
    """
    # TODO: Implement
    pass


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """
    Get a single task by id.

    Raise HTTPException(404) if not found.
    """
    # TODO: Implement
    pass


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updates: TaskUpdate):
    """
    Update a task partially (only provided fields).

    - Only update fields that are not None in the request
    - Raise HTTPException(404) if task not found
    - Return the updated task
    """
    # TODO: Implement
    pass


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """
    Delete a task by id.

    Raise HTTPException(404) if not found.
    Return 204 No Content on success.
    """
    # TODO: Implement
    pass


@app.get("/tasks/stats/summary")
def task_stats():
    """
    Return summary statistics.

    Return: {
        "total": int,
        "done": int,
        "pending": int,
        "avg_priority": float (rounded to 1 decimal)
    }
    """
    # TODO: Implement
    pass


# ============================================================
# Tests — run with: python lab_02_api.py
# ============================================================

def test_api():
    from fastapi.testclient import TestClient
    client = TestClient(app)

    # Clear state
    tasks_db.clear()
    global next_id
    next_id = 1

    # Create
    resp = client.post("/tasks", json={"title": "Write tests", "priority": 3})
    assert resp.status_code == 201
    task = resp.json()
    assert task["title"] == "Write tests"
    assert task["id"] == 1
    print("✓ POST /tasks works")

    # Read
    resp = client.get(f"/tasks/{task['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Write tests"
    print("✓ GET /tasks/{id} works")

    # Update
    resp = client.patch(f"/tasks/{task['id']}", json={"done": True})
    assert resp.status_code == 200
    assert resp.json()["done"] is True
    print("✓ PATCH /tasks/{id} works")

    # List with filter
    client.post("/tasks", json={"title": "Second task", "priority": 1})
    resp = client.get("/tasks?done=false")
    assert resp.status_code == 200
    assert len(resp.json()) == 1
    print("✓ GET /tasks with filter works")

    # Not found
    resp = client.get("/tasks/999")
    assert resp.status_code == 404
    print("✓ 404 handling works")

    # Delete
    resp = client.delete(f"/tasks/{task['id']}")
    assert resp.status_code == 204
    print("✓ DELETE /tasks/{id} works")

    print("\nAll API tests passed! ✓")


if __name__ == "__main__":
    test_api()
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run the tests with `python lab_02_api.py`
- [ ] (Stretch) Start the server with `uvicorn lab_02_api:app --reload` and test with the interactive docs at `http://localhost:8000/docs`
