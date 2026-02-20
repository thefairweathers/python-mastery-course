# Week 3: Control Flow & Logic

> **Goal:** Master Python's conditional statements, loops, and comprehensions — the tools that give your programs the ability to make decisions and repeat actions.

[← Week 2: Python Fundamentals](../week-02/README.md) · [Week 4: Functions & Scope →](../week-04/README.md)

---

## 3.1 Conditional Execution: `if` / `elif` / `else`

Programs need to make decisions. The `if` statement lets your code take different paths based on conditions.

### Basic Structure

```python
temperature = 22

if temperature > 30:
    print("It's hot outside")
```

Let's break this apart:
- `temperature > 30` is the **condition** — a boolean expression that evaluates to `True` or `False`
- The colon `:` marks the end of the condition
- The indented block below is the **body** — the code that runs only if the condition is `True`

**Indentation is not optional in Python.** Other languages use braces `{}` to delimit blocks; Python uses indentation (4 spaces by convention). This enforces readable code — your code's visual structure matches its logical structure.

### Adding Alternatives

```python
temperature = 22

if temperature > 30:
    print("It's hot outside")
elif temperature > 20:
    print("It's pleasant")
elif temperature > 10:
    print("It's cool")
else:
    print("It's cold")
```

Python evaluates conditions **from top to bottom** and runs the first block whose condition is `True`. Once a match is found, all remaining `elif`/`else` blocks are skipped.

In this example, `temperature` is 22. The first condition (`22 > 30`) is `False`, so Python moves on. The second (`22 > 20`) is `True`, so it prints "It's pleasant" and skips everything below.

### The Ternary Expression

For simple if/else assignments, Python offers a one-line form:

```python
age = 20
status = "adult" if age >= 18 else "minor"
```

Read this as: "status is 'adult' *if* age >= 18, *else* 'minor'." Use this for simple cases; for anything complex, stick with the full `if`/`else` block.

### Combining Conditions

Use `and`, `or`, and `not` to combine conditions:

```python
age = 25
has_license = True

if age >= 16 and has_license:
    print("Can drive")

if age < 13 or age > 65:
    print("Special pricing available")

if not has_license:
    print("Cannot drive")
```

**Operator precedence:** `not` binds tightest, then `and`, then `or`. Use parentheses when in doubt:

```python
# Without parentheses — 'and' evaluates before 'or'
if a or b and c:       # Means: a or (b and c)

# With parentheses — explicit and clear
if (a or b) and c:     # Different meaning!
```

---

## 3.2 Pattern Matching (Python 3.10+)

Pattern matching is Python's version of a `switch`/`case` statement, but much more powerful. It can match not just values, but also structures, types, and conditions.

### Basic Value Matching

```python
command = "quit"

match command:
    case "quit":
        print("Exiting program")
    case "help":
        print("Showing help menu")
    case "status":
        print("All systems operational")
    case _:
        print(f"Unknown command: {command}")
```

The `_` is a wildcard — it matches anything. It's like the `else` in an `if` chain.

### Structural Matching

This is where pattern matching gets powerful. You can match and decompose data structures:

```python
command = "go north"

match command.split():
    case ["quit"]:
        print("Quitting")
    case ["go", direction]:
        print(f"Moving {direction}")
    case ["pick", "up", item]:
        print(f"Picked up {item}")
    case _:
        print("I don't understand")
```

When `command.split()` produces `["go", "north"]`, the pattern `["go", direction]` matches it — binding the variable `direction` to `"north"`.

### Matching with Guards

You can add `if` conditions (called "guards") to patterns:

```python
def classify_number(n):
    match n:
        case 0:
            return "zero"
        case n if n > 0:
            return "positive"
        case n if n < 0:
            return "negative"
```

### Matching Dictionaries

```python
response = {"status": 200, "data": {"name": "Alice"}}

match response:
    case {"status": 200, "data": data}:
        print(f"Success! Data: {data}")
    case {"status": 404}:
        print("Not found")
    case {"status": status} if status >= 500:
        print(f"Server error: {status}")
```

Dictionary patterns match if the specified keys are present — extra keys are allowed and ignored.

---

## 3.3 Loops: `for` and `while`

### The `for` Loop

Python's `for` loop is fundamentally different from C-style `for(i=0; i<10; i++)`. In Python, `for` iterates over **any iterable** — a list, string, range, file, dictionary, or any object that produces values one at a time.

```python
# Iterating over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

Each time through the loop, `fruit` is assigned the next value from the list. After processing all values, the loop ends.

**`range()` for numeric loops.** When you need to loop a specific number of times:

```python
for i in range(5):
    print(i)
# Output: 0, 1, 2, 3, 4
```

`range(5)` generates the integers 0 through 4 (not 5 — the stop value is exclusive, just like slicing). You can also specify start, stop, and step:

```python
for i in range(2, 10, 3):
    print(i)
# Output: 2, 5, 8
```

### `enumerate()` — When You Need Both Index and Value

A common need is to loop over a collection while also tracking the position:

```python
# DON'T do this (un-Pythonic)
fruits = ["apple", "banana", "cherry"]
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# DO this instead (Pythonic)
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
```

`enumerate()` produces pairs of `(index, value)` from any iterable. The `i, fruit` syntax is called **unpacking** — it assigns the first element of each pair to `i` and the second to `fruit`.

You can start the counter at a number other than 0:

```python
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# Output:
# 1. apple
# 2. banana
# 3. cherry
```

### `zip()` — Iterating Over Multiple Sequences

When you need to process two (or more) sequences in parallel:

```python
names = ["Alice", "Bob", "Charlie"]
scores = [95, 87, 92]

for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

`zip()` pairs up elements from each iterable. It stops when the shortest one runs out.

### The `while` Loop

`while` loops repeat as long as a condition remains `True`:

```python
count = 0
while count < 5:
    print(count)
    count += 1
```

Use `while` when you don't know in advance how many iterations you need — for example, reading input until the user types "quit", or waiting for a condition to change.

**Caution:** A `while` loop runs forever if the condition never becomes `False`. Always make sure something inside the loop changes the condition.

### `break` and `continue`

`break` exits the loop immediately. `continue` skips to the next iteration:

```python
for i in range(100):
    if i % 2 == 0:
        continue          # Skip even numbers — jump to next iteration
    if i > 10:
        break             # Stop the loop entirely when i exceeds 10
    print(i)
# Output: 1, 3, 5, 7, 9
```

### The `for`/`else` Pattern

Python has an unusual feature: you can put an `else` block after a `for` loop. The `else` runs only if the loop completed **without** hitting a `break`:

```python
# Find the first even number
numbers = [1, 3, 5, 7, 9]

for num in numbers:
    if num % 2 == 0:
        print(f"Found even number: {num}")
        break
else:
    # This runs because no 'break' was executed
    print("No even numbers found")
```

This is most useful for search patterns — "look for something, and do X if it wasn't found."

---

## 3.4 Comprehensions

Comprehensions are a concise, Pythonic way to create collections. They're one of Python's most distinctive features, and you'll use them constantly once they click.

### List Comprehensions

The basic pattern replaces a for-loop-with-append:

```python
# The loop version
squares = []
for x in range(10):
    squares.append(x ** 2)

# The comprehension version — same result, more concise
squares = [x ** 2 for x in range(10)]
```

Read it as: "a list of `x ** 2` for each `x` in `range(10)`."

### Adding a Filter

You can add an `if` clause to include only items that match a condition:

```python
# Only even squares
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

Read it as: "a list of `x ** 2` for each `x` in `range(10)` *if* `x` is even."

### Transform with Conditional

An `if`/`else` **before** the `for` transforms every item (no filtering):

```python
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']
```

**Important distinction:**
- `[expr for x in iterable if condition]` — **filters** (some items excluded)
- `[expr_if_true if condition else expr_if_false for x in iterable]` — **transforms** (all items included)

### Dict and Set Comprehensions

The same syntax works for dictionaries and sets:

```python
# Dict comprehension
word_lengths = {word: len(word) for word in ["hello", "world", "python"]}
# {'hello': 5, 'world': 5, 'python': 6}

# Set comprehension (like list but with curly braces — produces unique values)
unique_lengths = {len(word) for word in ["hello", "world", "python"]}
# {5, 6}
```

### Generator Expressions

Replace `[]` with `()` to get a **generator expression**, which computes values lazily (one at a time) instead of building the entire list in memory:

```python
# This creates a list of 1 million items in memory
total = sum([x ** 2 for x in range(1_000_000)])

# This computes values one at a time — uses almost no memory
total = sum(x ** 2 for x in range(1_000_000))
```

The second form is preferred when you're passing the result to a function like `sum()`, `max()`, or `any()` that consumes items one at a time.

### When NOT to Use Comprehensions

Comprehensions are great for simple transformations and filters. But if your logic requires multiple steps, temporary variables, or error handling, use a regular loop — readability is more important than conciseness.

```python
# Too complex for a comprehension — use a loop
results = []
for item in data:
    try:
        value = transform(item)
        if validate(value):
            results.append(value)
    except ValueError:
        continue
```

---

## Labs

Complete the labs in the [labs/](labs/) directory:

- **[Lab 3.1: FizzBuzz Three Ways](labs/lab_01_fizzbuzz.py)** — Implement FizzBuzz using loops, comprehensions, and pattern matching
- **[Lab 3.2: Data Filter Pipeline](labs/lab_02_filter.py)** — Process and analyze a dataset using comprehensions and control flow

---

## Checklist

Before moving to Week 4, confirm you understand:

- [ ] `if`/`elif`/`else` and how Python evaluates conditions top-to-bottom
- [ ] Pattern matching with `match`/`case`, including structural and dictionary patterns
- [ ] The difference between `for` (iterate over something) and `while` (repeat while condition is true)
- [ ] `enumerate()`, `zip()`, `break`, `continue`, and `for`/`else`
- [ ] List, dict, and set comprehensions — and when to use a regular loop instead
- [ ] Generator expressions for memory-efficient processing

---

[← Week 2: Python Fundamentals](../week-02/README.md) · [Week 4: Functions & Scope →](../week-04/README.md)
