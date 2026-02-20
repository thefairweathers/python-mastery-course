# Week 8: Error Handling & Debugging

> **Goal:** Write resilient code that handles failures gracefully. Master Python's exception system, build custom exceptions, and learn debugging techniques.

[← Week 7: File I/O](../week-07/README.md) · [Week 9: Modules & Packages →](../week-09/README.md)

---

## 8.1 Why Error Handling Matters

Every program encounters errors: files that don't exist, network connections that time out, user input that's malformed, division by zero. The question isn't *whether* errors will happen — it's *how* your program responds when they do.

Without error handling, a single unexpected input can crash your entire program. With proper error handling, your program can recover gracefully, provide useful feedback, and continue running.

---

## 8.2 The Exception Hierarchy

Python organizes exceptions in a class hierarchy. Understanding this hierarchy helps you catch exceptions at the right level of specificity:

```
BaseException                 ← Don't catch this (includes SystemExit, KeyboardInterrupt)
└── Exception                 ← Catch this for "regular" errors
    ├── ValueError            ← Invalid value (e.g., int("abc"))
    ├── TypeError             ← Wrong type (e.g., "hello" + 5)
    ├── KeyError              ← Missing dict key
    ├── IndexError            ← List index out of range
    ├── FileNotFoundError     ← File doesn't exist
    ├── ConnectionError       ← Network failure
    └── ...many more...
```

**Never catch `BaseException`** — it would swallow `KeyboardInterrupt` (Ctrl+C) and `SystemExit`, making your program impossible to stop.

---

## 8.3 try / except / else / finally

### Basic Pattern

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
```

The `try` block contains code that might raise an exception. If an exception occurs, Python immediately jumps to the matching `except` block.

### Catching the Exception Object

```python
try:
    value = int("not a number")
except ValueError as e:
    print(f"Conversion failed: {e}")
    # Output: Conversion failed: invalid literal for int() with base 10: 'not a number'
```

The `as e` binds the exception object to `e`, giving you access to the error message.

### Multiple Exception Types

```python
try:
    data = {"key": "value"}
    result = int(data["missing_key"])
except KeyError as e:
    print(f"Missing key: {e}")
except ValueError as e:
    print(f"Invalid value: {e}")
except (TypeError, AttributeError) as e:
    print(f"Type/attribute error: {e}")
```

Python tries each `except` block in order. Only the first matching handler runs. **Order matters:** put more specific exceptions before general ones.

### The `else` Block

The `else` block runs only if **no exception** occurred in the `try` block:

```python
try:
    value = int(user_input)
except ValueError:
    print("Please enter a valid number")
else:
    # Only runs if int() succeeded
    print(f"You entered: {value}")
    process(value)
```

**Why not just put the code in `try`?** Because code in `else` won't have its exceptions caught by the `except` blocks above. This prevents accidentally catching exceptions from code that shouldn't raise them.

### The `finally` Block

`finally` **always runs** — whether an exception occurred or not, whether it was caught or not:

```python
def read_data(filename):
    f = None
    try:
        f = open(filename)
        return f.read()
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return None
    finally:
        if f:
            f.close()
        print("Cleanup complete")  # Always prints
```

In practice, use `with` statements instead of `finally` for resource cleanup. But `finally` is useful for logging, metrics, or resetting state.

---

## 8.4 Custom Exceptions

For any non-trivial application, define your own exception hierarchy. This lets callers handle your errors specifically:

```python
class AppError(Exception):
    """Base exception for our application."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")

class NotFoundError(AppError):
    """Raised when a requested resource doesn't exist."""
    def __init__(self, resource: str, identifier):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier}")
```

Using them:

```python
def get_user(user_id: int) -> dict:
    if user_id < 0:
        raise ValidationError("user_id", "Must be non-negative")
    if user_id not in database:
        raise NotFoundError("User", user_id)
    return database[user_id]

# Callers can handle at the level they want:
try:
    user = get_user(-1)
except ValidationError as e:
    print(f"Bad input: {e.field} — {e.message}")
except NotFoundError as e:
    print(f"Not found: {e.resource} #{e.identifier}")
except AppError as e:
    print(f"Application error: {e}")    # Catches any AppError subclass
```

---

## 8.5 Debugging Techniques

### The `logging` Module

`print()` statements work for quick debugging but don't scale. The `logging` module gives you severity levels, timestamps, and the ability to turn debugging output on/off:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

logger = logging.getLogger(__name__)

def process_item(item):
    logger.debug(f"Processing: {item}")
    if item < 0:
        logger.warning(f"Negative value: {item}")
    logger.info("Item processed")
```

Levels from least to most severe: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Set the level to control what gets printed.

### `breakpoint()` — The Built-in Debugger

Python 3.7+ includes `breakpoint()`, which drops you into an interactive debugger:

```python
def buggy_function(data):
    for item in data:
        result = item * 2
        breakpoint()          # Execution pauses here
        print(result)
```

In the debugger (pdb), you can inspect variables, step through code, and evaluate expressions:
- `n` — next line
- `s` — step into function call
- `c` — continue execution
- `p variable` — print a variable's value
- `q` — quit the debugger

---

## Labs

- **[Lab 8.1: Resilient Processor](labs/lab_01_processor.py)** — Build a data processor that handles errors gracefully and generates reports
- **[Lab 8.2: Custom Exception Hierarchy](labs/lab_02_exceptions.py)** — Design and implement a custom exception system for a REST API

---

## Checklist

- [ ] Use `try`/`except`/`else`/`finally` correctly
- [ ] Catch specific exceptions, never bare `except:`
- [ ] Design custom exception hierarchies for your applications
- [ ] Use `logging` instead of `print()` for debugging
- [ ] Use `breakpoint()` to step through code interactively

---

[← Week 7: File I/O](../week-07/README.md) · [Week 9: Modules & Packages →](../week-09/README.md)
