# Week 7: File I/O & Data Formats

> **Goal:** Read and write files confidently, work with JSON and CSV, and use `pathlib` for modern file system operations.

[← Week 6: OOP](../week-06/README.md) · [Week 8: Error Handling & Debugging →](../week-08/README.md)

---

## 7.1 Context Managers and the `with` Statement

Before we talk about reading files, you need to understand **resource management**. Opening a file consumes an operating system resource (a file descriptor). If you don't close it, you leak that resource. Leaking enough of them crashes your program.

Python's `with` statement guarantees cleanup:

```python
with open("example.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("Line two.\n")
# File is automatically closed here — even if an exception occurred
```

**How it works internally:** When entering the `with` block, Python calls `f.__enter__()`. When leaving (normally or via exception), it calls `f.__exit__()`, which closes the file. You never need to remember to close it yourself.

**The rule:** Always use `with` for files, database connections, network sockets, and any resource that needs cleanup.

---

## 7.2 Reading and Writing Text Files

### Writing

The `open()` function's second argument is the **mode**:

| Mode | Meaning |
|------|---------|
| `"r"` | Read (default) — file must exist |
| `"w"` | Write — creates or **overwrites** |
| `"a"` | Append — creates or adds to end |
| `"x"` | Exclusive create — fails if file exists |

```python
# Write (creates new file or OVERWRITES existing)
with open("notes.txt", "w") as f:
    f.write("First line\n")
    f.write("Second line\n")

# Append (adds to existing file)
with open("notes.txt", "a") as f:
    f.write("Third line\n")
```

### Reading

Three approaches, each suited to different situations:

```python
# Approach 1: Read entire file as one string
with open("notes.txt", "r") as f:
    content = f.read()
print(content)

# Approach 2: Read all lines into a list
with open("notes.txt", "r") as f:
    lines = f.readlines()       # Each line includes the '\n'
print(lines)

# Approach 3: Iterate line by line (memory-efficient for large files)
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())     # .strip() removes the trailing '\n'
```

Approach 3 is preferred for large files because it only holds one line in memory at a time. Approaches 1 and 2 load the entire file into memory.

---

## 7.3 pathlib — Modern Path Handling

The `pathlib` module (Python 3.4+) provides an object-oriented interface for file paths. It replaces the older `os.path` module and is much more readable.

```python
from pathlib import Path
```

### Creating Paths

```python
home = Path.home()                              # /Users/<you>
project = Path("~/dev/my-project").expanduser()  # Expand ~ to home dir
config = project / "config" / "settings.json"   # The / operator joins paths
```

The `/` operator is overloaded on Path objects to join path segments. This is much cleaner than `os.path.join("config", "settings.json")`.

### Inspecting Paths

```python
path = Path("data/reports/q4_results.csv")

path.name           # 'q4_results.csv'    — filename with extension
path.stem           # 'q4_results'        — filename without extension
path.suffix         # '.csv'              — extension
path.parent         # PosixPath('data/reports')
path.exists()       # True or False
path.is_file()      # True or False
path.is_dir()       # True or False
```

### File Operations with pathlib

```python
path = Path("example.txt")

# Write and read (convenience methods for small files)
path.write_text("Hello from pathlib!")
content = path.read_text()

# Create directories
Path("data/output").mkdir(parents=True, exist_ok=True)

# Find files by pattern
for py_file in Path(".").rglob("*.py"):   # Recursive glob
    print(py_file)

# Delete
path.unlink(missing_ok=True)              # Delete file (no error if missing)
```

---

## 7.4 JSON — JavaScript Object Notation

JSON is the universal data interchange format. Python's `json` module handles serialization (Python objects → JSON string) and deserialization (JSON string → Python objects).

### The Type Mapping

| Python | JSON |
|--------|------|
| `dict` | `object {}` |
| `list` | `array []` |
| `str` | `string` |
| `int`, `float` | `number` |
| `True` / `False` | `true` / `false` |
| `None` | `null` |

### Writing and Reading JSON

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "SQL", "Docker"],
    "active": True,
    "address": None,
}

# Write to file
with open("user.json", "w") as f:
    json.dump(data, f, indent=2)

# Read from file
with open("user.json", "r") as f:
    loaded = json.load(f)

print(loaded["name"])      # 'Alice'
print(type(loaded["age"])) # <class 'int'> — types are preserved
```

The `indent=2` parameter makes the output human-readable with 2-space indentation.

### Handling Types JSON Doesn't Support

JSON can't represent `datetime`, `set`, `bytes`, or custom classes. You need to convert them:

```python
from datetime import datetime

# Custom encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

event = {"name": "Meeting", "time": datetime.now()}
json_str = json.dumps(event, cls=DateTimeEncoder, indent=2)
```

---

## 7.5 CSV — Comma-Separated Values

CSV files are the lingua franca of tabular data. Python's `csv` module handles quoting, escaping, and edge cases that naive string splitting would miss.

### Writing CSV

```python
import csv

headers = ["name", "department", "salary"]
employees = [
    ["Alice", "Engineering", 95000],
    ["Bob", "Marketing", 72000],
    ["Charlie", "Engineering", 88000],
]

with open("employees.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)       # Write header row
    writer.writerows(employees)    # Write all data rows
```

The `newline=""` parameter prevents double-spaced output on Windows.

### Reading CSV as Dictionaries

```python
with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)     # Uses first row as field names
    for row in reader:
        name = row["name"]
        salary = int(row["salary"])  # CSV values are always strings!
        print(f"{name} earns ${salary:,}")
```

`DictReader` is almost always preferred over plain `csv.reader` because it gives you column access by name instead of position.

---

## Labs

- **[Lab 7.1: Config Manager](labs/lab_01_config.py)** — Build a layered config system (defaults → file → environment variables)
- **[Lab 7.2: Log Parser](labs/lab_02_logs.py)** — Parse and analyze a log file using file I/O and data structures

---

## Checklist

- [ ] Always use `with` for file operations — explain why
- [ ] Read files three ways: `.read()`, `.readlines()`, and line iteration
- [ ] Use `pathlib.Path` for all path operations (joining, inspecting, globbing)
- [ ] Serialize/deserialize JSON with `json.dump`/`json.load`
- [ ] Read/write CSV with `csv.DictReader`/`csv.DictWriter`
- [ ] Handle types that JSON doesn't support natively

---

[← Week 6: OOP](../week-06/README.md) · [Week 8: Error Handling & Debugging →](../week-08/README.md)
