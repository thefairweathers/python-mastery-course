---
title: "Week 4: Functions & Scope"
sidebar:
  order: 0
---


> **Goal:** Understand how to define, compose, and use functions — the primary building block of well-organized Python code. Master scope, closures, and first-class functions.


---

## 4.1 Why Functions Matter

Every program of any complexity needs to be broken into smaller pieces. Functions serve three purposes:

1. **Reuse** — Write code once, call it many times
2. **Abstraction** — Give a name to a complex operation so you can think about *what* it does without worrying about *how*
3. **Isolation** — Variables inside a function don't leak out and interfere with the rest of your program

A well-written function does one thing, has a clear name that describes what it does, takes inputs as parameters, and returns a result.

---

## 4.2 Defining Functions

### Basic Structure

```python
def greet(name):
    """Return a greeting string for the given name."""
    return f"Hello, {name}!"
```

Let's break this apart piece by piece:

- **`def`** — The keyword that starts a function definition
- **`greet`** — The function's name. By convention, Python functions use `snake_case`
- **`(name)`** — The parameter list. `name` is a parameter — a placeholder that will receive a value when the function is called
- **`"""`** — A docstring. This documents what the function does. It's accessible via `help(greet)` and used by IDEs for autocompletion hints
- **`return`** — Sends a value back to the caller. Without `return`, a function returns `None`

Calling the function:

```python
result = greet("Tim")
print(result)           # "Hello, Tim!"
```

When you call `greet("Tim")`, Python creates a local variable `name` with the value `"Tim"`, runs the function body, and returns the result.

### Type Hints

Type hints document what types a function expects and returns. Python doesn't enforce them at runtime, but they make your code more readable and enable tools like `mypy` to catch type errors before you run the code.

```python
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b
```

The `-> int` annotation says this function returns an integer. This is documentation, not enforcement — `add("hello", " world")` would still work (returning `"hello world"`), but `mypy` would flag it as a type error.

### Default Arguments

You can give parameters default values. Parameters with defaults become optional:

```python
def create_user(name: str, role: str = "viewer", active: bool = True) -> dict:
    """Create a user dictionary with the given properties."""
    return {"name": name, "role": role, "active": active}
```

```python
create_user("Alice")                         # Uses both defaults
create_user("Bob", role="admin")             # Overrides role
create_user("Charlie", active=False)         # Overrides active
create_user("Diana", "editor", False)        # Positional overrides (order matters)
```

Parameters without defaults (like `name`) must come before parameters with defaults.

### The Mutable Default Argument Trap

This is one of Python's most infamous gotchas:

```python
def add_item(item, items=[]):     # DON'T DO THIS
    items.append(item)
    return items

print(add_item("a"))   # ['a']       — looks fine
print(add_item("b"))   # ['a', 'b']  — BUG! The list persists!
```

**Why this happens:** The default value `[]` is created *once* when the function is defined, not each time the function is called. Every call shares the same list object.

**The fix:** Use `None` as the default and create a new list inside the function:

```python
def add_item(item, items=None):   # DO THIS
    if items is None:
        items = []
    items.append(item)
    return items
```

This pattern applies to any mutable default: lists, dicts, sets.

---

## 4.3 Argument Patterns

Python offers several ways to pass arguments. Understanding these gives you flexibility in designing function interfaces.

### `*args` — Variable Positional Arguments

The `*args` syntax collects any number of positional arguments into a tuple:

```python
def total(*numbers):
    """Sum any number of arguments."""
    return sum(numbers)

total(1, 2, 3)         # 6
total(10, 20)           # 30
total(5)                # 5
```

Inside the function, `numbers` is a tuple: `(1, 2, 3)`.

### `**kwargs` — Variable Keyword Arguments

The `**kwargs` syntax collects any number of keyword arguments into a dictionary:

```python
def create_tag(tag_name, **attributes):
    """Build an HTML tag with dynamic attributes."""
    attrs = " ".join(f'{k}="{v}"' for k, v in attributes.items())
    return f"<{tag_name} {attrs}>"

create_tag("div", id="main", class_="container")
# '<div id="main" class_="container">'
```

### Keyword-Only Arguments

Placing a bare `*` in the parameter list forces all subsequent parameters to be passed by keyword:

```python
def connect(*, host: str, port: int, timeout: int = 30):
    """All arguments must be passed by name."""
    print(f"Connecting to {host}:{port} (timeout={timeout}s)")

connect(host="localhost", port=5432)          # Works
# connect("localhost", 5432)                  # TypeError — must use keywords
```

This is excellent for functions with many options — it forces callers to be explicit, preventing bugs from misordered arguments.

---

## 4.4 Scope and the LEGB Rule

When Python encounters a variable name, it searches for it in four places, in this order:

1. **L**ocal — inside the current function
2. **E**nclosing — inside any enclosing (outer) functions
3. **G**lobal — at the module (file) level
4. **B**uilt-in — Python's built-in names (`print`, `len`, `range`, etc.)

This is called the **LEGB rule**:

```python
x = "global"              # Global scope

def outer():
    x = "enclosing"       # Enclosing scope

    def inner():
        x = "local"       # Local scope
        print(x)          # → "local"

    inner()
    print(x)              # → "enclosing"

outer()
print(x)                  # → "global"
```

Each function has its own local scope. Assigning to a variable inside a function creates it in the local scope, even if a variable with the same name exists in an outer scope.

---

## 4.5 Closures

A **closure** occurs when an inner function captures variables from an enclosing function's scope, and that inner function is returned or passed elsewhere. The captured variables "live on" even after the enclosing function has finished executing.

```python
def make_multiplier(factor):
    """Return a function that multiplies its input by factor."""
    def multiply(n):
        return n * factor     # 'factor' is captured from the enclosing scope
    return multiply
```

Let's trace what happens:

```python
double = make_multiplier(2)
```

1. `make_multiplier(2)` runs with `factor = 2`
2. It defines `multiply` — a function that uses `factor`
3. It returns `multiply` (the function object itself, not a call to it)
4. `double` now holds a function that remembers `factor = 2`

```python
print(double(5))    # 10
print(double(100))  # 200

triple = make_multiplier(3)
print(triple(5))    # 15
```

Each call to `make_multiplier` creates a **new** closure with its own captured `factor`. `double` and `triple` are independent functions with different captured values.

---

## 4.6 Functions as First-Class Objects

In Python, functions are objects — just like integers, strings, and lists. This means you can:

```python
# Assign functions to variables
say_hello = greet
print(say_hello("Tim"))

# Store functions in data structures
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
}
print(operations["add"](10, 3))   # 13

# Pass functions as arguments
def apply_twice(func, value):
    return func(func(value))

print(apply_twice(lambda x: x * 2, 3))    # 12: (3 * 2) * 2

# Return functions from functions (this is closures!)
```

### Lambda Functions

Lambdas are anonymous, single-expression functions. They're useful as quick callbacks:

```python
# Sort a list of tuples by the second element
students = [("Alice", 92), ("Bob", 78), ("Charlie", 95)]
by_grade = sorted(students, key=lambda s: s[1], reverse=True)
# [('Charlie', 95), ('Alice', 92), ('Bob', 78)]
```

**Rule of thumb:** If a lambda needs a name (i.e., you're assigning it to a variable), use a `def` instead. Lambdas are for inline use.

---

## Labs

- **[Lab 4.1: Memoization](./lab-01-memoize)** — Build a caching decorator from scratch
- **[Lab 4.2: Data Pipeline](./lab-02-pipeline)** — Compose functions into a text processing pipeline

---

## Checklist

- [ ] Define functions with type hints, defaults, `*args`, and `**kwargs`
- [ ] Explain the mutable default argument trap and its fix
- [ ] Trace variable lookup using the LEGB rule
- [ ] Create closures that capture variables from enclosing scope
- [ ] Use functions as first-class objects: pass as arguments, return from functions
- [ ] Use `lambda` appropriately for short inline callbacks

---

