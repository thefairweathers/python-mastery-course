---
title: "Week 10: Testing & Code Quality"
sidebar:
  order: 0
---


> **Goal:** Write tests with pytest, use fixtures and parametrize, and set up code quality tools (formatting, linting, type checking).


---

## 10.1 Why Test?

Tests serve three purposes that no amount of manual checking can replace:

1. **Catch regressions** — When you change code, tests tell you instantly if you broke something that used to work.
2. **Document behavior** — Tests show exactly what your code is supposed to do, with concrete examples.
3. **Enable fearless refactoring** — With good tests, you can restructure code confidently, knowing you'll catch mistakes immediately.

---

## 10.2 pytest Fundamentals

Install pytest:

```bash
pip install pytest
```

### Your First Test

Create a file called `test_math.py` (pytest discovers files starting with `test_`):

```python
# test_math.py

def add(a, b):
    return a + b

def test_add_positive():
    assert add(2, 3) == 5
```

The `assert` statement checks that a condition is `True`. If it's `False`, the test fails and pytest shows you what went wrong.

Run it:

```bash
pytest test_math.py -v
```

The `-v` flag gives verbose output showing each test name and status.

### Testing Exceptions

To verify that code raises the correct exception:

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
```

`pytest.raises` acts as a context manager that catches the expected exception. If the exception isn't raised, the test fails. The `match` parameter checks the error message against a regex pattern.

### Parametrize — Run One Test with Many Inputs

Instead of writing a separate test for every input combination, `@pytest.mark.parametrize` runs the same test with different data:

```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
    (-5, -3, -8),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

This generates 5 separate test cases from one function. Each row of the parameter list becomes a test run.

### Fixtures — Shared Test Setup

**Fixtures** provide reusable setup for tests. Instead of repeating setup code in every test, define it once:

```python
import pytest

@pytest.fixture
def sample_users():
    """Provide a list of sample users for tests."""
    return [
        {"name": "Alice", "age": 30, "role": "admin"},
        {"name": "Bob", "age": 25, "role": "user"},
        {"name": "Charlie", "age": 35, "role": "user"},
    ]

def test_user_count(sample_users):
    assert len(sample_users) == 3

def test_admin_exists(sample_users):
    admins = [u for u in sample_users if u["role"] == "admin"]
    assert len(admins) == 1
    assert admins[0]["name"] == "Alice"
```

pytest automatically injects the fixture by matching the parameter name (`sample_users`) to the fixture function name.

### Fixtures with Cleanup

Use `yield` in a fixture to run cleanup after the test:

```python
@pytest.fixture
def temp_database(tmp_path):
    """Create a temporary database file."""
    db_path = tmp_path / "test.db"
    db = create_database(db_path)
    yield db                           # Test runs here
    db.close()                         # Cleanup runs after test
```

### Float Comparisons

Use `pytest.approx` for floating-point comparisons:

```python
def test_division():
    assert 10 / 3 == pytest.approx(3.333, rel=1e-3)
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

---

## 10.3 Code Quality Tools

### Black — Code Formatting

Black is an opinionated formatter. It makes your code consistent without you thinking about style:

```bash
pip install black
black .               # Formats all .py files in the current directory
black --check .       # Check without modifying (for CI)
```

### Ruff — Linting

Ruff is an extremely fast Python linter that catches errors, style issues, and potential bugs:

```bash
pip install ruff
ruff check .          # Check for issues
ruff check . --fix    # Auto-fix where possible
```

### mypy — Type Checking

mypy verifies your type hints without running the code:

```bash
pip install mypy
mypy src/             # Check type annotations
```

### Running Everything Together

Add to your `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=src"

[tool.black]
line-length = 100

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
```

Then your workflow becomes:

```bash
black .              # Format
ruff check .         # Lint
mypy src/            # Type check
pytest               # Test
```

---

## Labs

- **[Lab 10.1: Test Suite](./lab-01-testing)** — Write a comprehensive test suite for a task manager module
- **[Lab 10.2: Quality Pipeline](./lab-02-quality)** — Set up black, ruff, mypy, and pytest for an existing project

---

## Checklist

- [ ] Write tests with `assert`, `pytest.raises`, and `pytest.approx`
- [ ] Use `@pytest.mark.parametrize` to test multiple inputs
- [ ] Create fixtures for shared test setup and cleanup
- [ ] Run tests with coverage: `pytest --cov`
- [ ] Format code with Black, lint with Ruff, type-check with mypy

---

