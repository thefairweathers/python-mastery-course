---
title: "Week 12: APIs & Data Engineering"
sidebar:
  order: 0
---


> **Goal:** Make HTTP requests, build REST APIs with FastAPI, and process data with pandas. These are the skills that connect Python to the real world.


---

## 12.1 Making HTTP Requests

Most modern applications consume APIs — fetching data from web services, posting updates, authenticating users. The `requests` library makes this straightforward.

```bash
pip install requests
```

### GET Requests

```python
import requests

response = requests.get("https://api.github.com/users/python")
```

The `response` object contains everything the server sent back. Let's examine it:

```python
print(response.status_code)                # 200 (success)
print(response.headers["content-type"])     # 'application/json; charset=utf-8'
data = response.json()                      # Parse JSON body into a Python dict
print(data["name"])                         # 'Python'
print(data["public_repos"])                 # Number of public repos
```

### POST Requests

To send data to a server:

```python
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "Alice", "role": "engineer"},    # Automatically serialized to JSON
    headers={"Authorization": "Bearer token123"},
    timeout=10,                                     # Fail after 10 seconds
)
```

### Error Handling

Always handle network failures:

```python
try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()     # Raises HTTPError for 4xx/5xx responses
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

`raise_for_status()` is a convenience method — it checks the status code and raises an exception for any error response, so you don't have to check manually.

---

## 12.2 Building APIs with FastAPI

FastAPI is a modern Python framework for building web APIs. It uses type hints for automatic validation, documentation, and serialization.

```bash
pip install fastapi uvicorn
```

### Your First API

Create `api.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.get("/greet/{name}")
def greet(name: str):
    return {"greeting": f"Hello, {name}!"}
```

Run it:

```bash
uvicorn api:app --reload
```

Open `http://localhost:8000` in your browser. Visit `http://localhost:8000/docs` for auto-generated interactive documentation.

### Request Validation with Pydantic

FastAPI uses Pydantic models for automatic request/response validation:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

# Define the data model
class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    body: str = Field(default="")
    tags: list[str] = Field(default_factory=list)

class Note(NoteCreate):
    id: int

# In-memory storage
notes: dict[int, Note] = {}
next_id = 1

@app.post("/notes", response_model=Note, status_code=201)
def create_note(data: NoteCreate):
    global next_id
    note = Note(id=next_id, **data.model_dump())
    notes[next_id] = note
    next_id += 1
    return note

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return notes[note_id]
```

FastAPI automatically validates incoming JSON against the `NoteCreate` model. If the title is missing or too long, the client gets a clear 422 error with details — no manual validation code needed.

---

## 12.3 Data Engineering with pandas

pandas is the standard tool for working with tabular data in Python.

```bash
pip install pandas matplotlib
```

### Creating DataFrames

A DataFrame is a table with labeled columns and rows:

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie", "Diana"],
    "department": ["Eng", "Sales", "Eng", "Sales"],
    "salary": [95000, 72000, 88000, 68000],
    "years": [5, 3, 7, 2],
})
```

### Exploration

```python
df.head()           # First 5 rows
df.info()           # Column types and null counts
df.describe()       # Statistical summary (mean, std, min, max, etc.)
df.shape            # (4, 4) — 4 rows, 4 columns
```

### Selection and Filtering

```python
# Select a column
df["name"]                          # Returns a Series

# Select multiple columns
df[["name", "salary"]]              # Returns a DataFrame

# Filter rows
engineers = df[df["department"] == "Eng"]
high_salary = df[df["salary"] > 80000]

# Combine conditions (use & for AND, | for OR, wrap each in parentheses)
senior_eng = df[(df["department"] == "Eng") & (df["years"] > 5)]
```

### Aggregation

```python
# Group by department and calculate statistics
summary = df.groupby("department").agg(
    avg_salary=("salary", "mean"),
    headcount=("name", "count"),
    avg_years=("years", "mean"),
)
print(summary)
```

### Adding and Transforming Columns

```python
df["bonus"] = df["salary"] * 0.1
df["level"] = df["years"].apply(
    lambda y: "Senior" if y > 5 else "Mid" if y > 3 else "Junior"
)
```

### Reading External Data

```python
# CSV
df = pd.read_csv("data.csv")

# JSON
df = pd.read_json("data.json")

# Excel
df = pd.read_excel("data.xlsx")

# Writing
df.to_csv("output.csv", index=False)
```

---

## 12.4 Data Visualization

```python
import matplotlib.pyplot as plt

# Simple line chart
months = ["Jan", "Feb", "Mar", "Apr", "May"]
revenue = [45000, 52000, 48000, 61000, 55000]

plt.figure(figsize=(10, 5))
plt.plot(months, revenue, marker="o", color="teal")
plt.title("Monthly Revenue")
plt.ylabel("Revenue ($)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("revenue.png", dpi=150)
plt.close()
```

pandas integrates directly with matplotlib:

```python
df.groupby("department")["salary"].mean().plot(kind="bar")
plt.title("Average Salary by Department")
plt.savefig("salary_by_dept.png")
```

---

## Labs

- **[Lab 12.1: API Client](./lab-01-api)** — Build a typed Python client for a REST API
- **[Lab 12.2: REST API](./lab-02-api)** — Build a task management API with FastAPI
- **[Lab 12.3: Data Analysis](./lab-03-analysis)** — Analyze a CSV dataset with pandas and create visualizations

---

## Checklist

- [ ] Make GET/POST requests with `requests`, handling errors and timeouts
- [ ] Build a FastAPI endpoint with Pydantic validation and auto-docs
- [ ] Create, filter, aggregate, and transform pandas DataFrames
- [ ] Generate charts with matplotlib and save them as images
- [ ] Read CSV/JSON/Excel data into pandas

---

