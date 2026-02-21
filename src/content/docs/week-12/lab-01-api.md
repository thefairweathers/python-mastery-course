---
title: "Lab 12.1: API Client"
sidebar:
  order: 1
---

> **Download:** [`lab_01_api.py`](/python-mastery-course/scaffolds/week-12/lab_01_api.py)

```python
"""
Lab 12.1: REST API — Build a notes API with FastAPI.
Run with: uvicorn lab_01_api:app --reload
TODO: Implement GET /notes, POST /notes, GET /notes/{id}, DELETE /notes/{id}
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Notes API")

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1)
    body: str = ""

class Note(NoteCreate):
    id: int

notes_db: dict[int, Note] = {}
next_id = 1

# TODO: Implement the endpoints

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
