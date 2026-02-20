# Week 9: Modules, Packages & Project Structure

> **Goal:** Organize your code into modules and packages, understand Python's import system, and learn professional project layout.

[← Week 8: Error Handling](../week-08/README.md) · [Week 10: Testing & Code Quality →](../week-10/README.md)

---

## 9.1 Why Structure Matters

A single Python file works fine for scripts under 200 lines. Beyond that, you need to split your code into **modules** (individual `.py` files) and **packages** (directories of modules). Good structure makes code navigable, testable, and maintainable.

---

## 9.2 Modules

A **module** is simply a `.py` file. When you import it, Python executes the file and makes its contents available to your code.

Create a file called `math_utils.py`:

```python
# math_utils.py
"""Utility functions for math operations."""

PI = 3.14159265358979

def circle_area(radius: float) -> float:
    """Calculate the area of a circle."""
    return PI * radius ** 2

def fahrenheit_to_celsius(f: float) -> float:
    """Convert Fahrenheit to Celsius."""
    return (f - 32) * 5 / 9
```

Now you can import it in another file:

```python
# main.py
import math_utils

area = math_utils.circle_area(5)
print(f"Area: {area:.2f}")
```

The `import math_utils` statement tells Python to:
1. Find `math_utils.py` (looking in the current directory, then `sys.path`)
2. Execute it (creating the `PI` variable, defining the functions)
3. Create a namespace `math_utils` so you access things as `math_utils.circle_area`

### Import Styles

```python
# Import the module — access via module.name
import math_utils
math_utils.circle_area(5)

# Import specific names — access directly
from math_utils import circle_area, PI
circle_area(5)

# Import with alias
import math_utils as mu
mu.circle_area(5)

# Import everything (avoid this — pollutes namespace)
from math_utils import *
```

---

## 9.3 Packages

A **package** is a directory containing an `__init__.py` file and one or more modules.

```
myproject/
├── __init__.py          ← Makes this directory a package
├── models.py
├── services.py
└── utils/
    ├── __init__.py      ← Nested package
    ├── formatting.py
    └── validation.py
```

The `__init__.py` file can be empty, or it can define what gets exported when someone imports the package:

```python
# myproject/__init__.py
"""MyProject — a sample Python package."""
__version__ = "0.1.0"

from .models import User, Order          # Re-export for convenience
from .services import process_order
```

The leading dot in `from .models import User` is a **relative import** — it means "from the `models` module *in this package*."

---

## 9.4 Professional Project Layout

Here's the standard layout for a Python project:

```
my-project/
├── .venv/                         # Virtual environment (git-ignored)
├── .gitignore
├── README.md
├── pyproject.toml                 # Project configuration (modern standard)
├── requirements.txt               # Pinned dependencies
├── src/
│   └── myproject/                 # Your package
│       ├── __init__.py
│       ├── __main__.py            # Entry point for python -m myproject
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py
│       │   └── services.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── conftest.py                # Shared test fixtures
│   ├── test_models.py
│   └── test_services.py
└── scripts/
    └── seed_data.py
```

**Key directories:**
- **`src/myproject/`** — Your actual package code. The `src/` layout prevents accidental imports of the package from the project root.
- **`tests/`** — All test files, named `test_*.py` so pytest discovers them automatically.
- **`scripts/`** — Utility scripts that aren't part of the package.

### `pyproject.toml`

This is the modern standard for Python project configuration (replacing `setup.py` and `setup.cfg`):

```toml
[project]
name = "myproject"
version = "0.1.0"
description = "A well-structured Python project"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "ruff>=0.1",
]

[project.scripts]
myproject = "myproject.__main__:main"
```

### The `__main__.py` Entry Point

This file lets your package be run with `python -m myproject`:

```python
# src/myproject/__main__.py
"""Entry point for: python -m myproject"""
from .core.services import main

if __name__ == "__main__":
    main()
```

---

## 9.5 The `.gitignore` for Python

```gitignore
# Virtual environments
.venv/
venv/

# Python cache
__pycache__/
*.pyc
*.pyo

# Distribution
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/

# OS
.DS_Store
```

---

## Labs

- **[Lab 9.1: CLI Notes App](labs/lab_01_notes/)** — Build a complete CLI application with proper package structure
- **[Lab 9.2: Package Publishing](labs/lab_02_packaging.md)** — Create a `pyproject.toml` and install your package in development mode

---

## Checklist

- [ ] Explain the difference between a module (file) and a package (directory)
- [ ] Use `import`, `from ... import`, and relative imports correctly
- [ ] Structure a project with `src/`, `tests/`, and `pyproject.toml`
- [ ] Create a `__main__.py` entry point
- [ ] Write a `.gitignore` for Python projects

---

[← Week 8: Error Handling](../week-08/README.md) · [Week 10: Testing & Code Quality →](../week-10/README.md)
