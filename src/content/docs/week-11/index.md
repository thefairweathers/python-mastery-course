---
title: "Week 11: Advanced Patterns"
sidebar:
  order: 0
---


> **Goal:** Master generators, decorators, and concurrency — the patterns that separate intermediate Python from advanced Python.


---

## 11.1 Generators

### The Problem Generators Solve

Imagine you need to process a 10GB log file. Loading it all into memory with `f.read()` or `list(f)` would crash your program. You need a way to process data **one piece at a time**.

Generators do exactly this. They produce values **lazily** — one at a time, on demand — using almost no memory regardless of how much data they process.

### Generator Functions

A generator function uses `yield` instead of `return`. Each time you call `next()` on it, it runs until the next `yield`, produces a value, and **pauses**:

```python
def countdown(n):
    """Generate a countdown from n to 1."""
    while n > 0:
        yield n        # Produce a value and pause
        n -= 1         # Resume here on next call
```

Let's trace the execution step by step:

```python
gen = countdown(3)     # Creates a generator object (nothing runs yet)

print(next(gen))       # Runs until first yield → prints 3
print(next(gen))       # Resumes, runs until next yield → prints 2
print(next(gen))       # Resumes → prints 1
# next(gen)            # Would raise StopIteration — generator is exhausted
```

In practice, you iterate with a `for` loop, which handles `StopIteration` automatically:

```python
for num in countdown(5):
    print(num)          # 5, 4, 3, 2, 1
```

### Memory Efficiency

```python
import sys

# List — ALL 1 million values in memory at once
big_list = [x ** 2 for x in range(1_000_000)]
print(f"List:      {sys.getsizeof(big_list):>10,} bytes")    # ~8.4 MB

# Generator — values computed one at a time
big_gen = (x ** 2 for x in range(1_000_000))
print(f"Generator: {sys.getsizeof(big_gen):>10,} bytes")     # ~200 bytes!
```

The generator uses the same amount of memory whether it generates 100 values or 100 billion.

### Generator Pipelines

The real power of generators is **chaining** them into data processing pipelines where each stage processes one item at a time:

```python
def read_lines(path):
    """Stage 1: Read file line by line."""
    with open(path) as f:
        for line in f:
            yield line.strip()

def filter_nonempty(lines):
    """Stage 2: Skip empty lines."""
    for line in lines:
        if line:
            yield line

def parse_numbers(lines):
    """Stage 3: Convert to integers."""
    for line in lines:
        try:
            yield int(line)
        except ValueError:
            continue

# Build the pipeline — no data flows until iteration begins
pipeline = parse_numbers(filter_nonempty(read_lines("data.txt")))

# Now data flows through all 3 stages, one line at a time
total = sum(pipeline)
```

Each stage processes exactly one item before passing it to the next. The entire file is never held in memory.

---

## 11.2 Decorators

### What Decorators Are

A decorator is a function that takes a function and returns a modified version. The `@decorator` syntax is shorthand for `func = decorator(func)`.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@my_decorator
def greet(name):
    print(f"Hello, {name}!")

greet("Tim")
# Output:
#   Calling greet
#   Hello, Tim!
#   Finished greet
```

The `@my_decorator` line is equivalent to writing `greet = my_decorator(greet)` after the function definition. The original `greet` function is replaced by `wrapper`, which adds behavior before/after calling the original.

### Practical Decorator: Timing

```python
import functools
import time

def timer(func):
    """Measure and print function execution time."""
    @functools.wraps(func)     # Preserve the original function's name and docstring
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.5)
    return "done"

slow_function()    # "slow_function took 0.5001s"
```

**`@functools.wraps(func)`** is critical — without it, the wrapper replaces the original function's `__name__`, `__doc__`, and other metadata, which breaks debugging and documentation tools.

### Decorators with Arguments

To make a decorator accept configuration, you need an extra level of nesting:

```python
def retry(max_attempts: int = 3, delay: float = 1.0):
    """Retry a function on failure."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_api_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Service unavailable")
    return {"status": "ok"}
```

The three layers: `retry(...)` returns `decorator`, which takes `func` and returns `wrapper`.

---

## 11.3 Concurrency with `async`/`await`

### The Problem

Many programs spend most of their time **waiting** — for network responses, file reads, database queries. Concurrency lets you do useful work while waiting, dramatically improving throughput.

### `asyncio` Basics

`async def` creates a **coroutine** — a function that can pause and resume:

```python
import asyncio

async def fetch_data(url: str, delay: float) -> dict:
    """Simulate an async HTTP request."""
    print(f"  Starting {url}")
    await asyncio.sleep(delay)          # Pause here (non-blocking)
    print(f"  Finished {url}")
    return {"url": url, "status": 200}
```

`await` pauses the coroutine and lets other coroutines run. This is different from `time.sleep()`, which blocks the entire thread.

### Sequential vs. Concurrent

```python
async def main():
    # Sequential — each request waits for the previous one
    # Total time: ~3 seconds
    r1 = await fetch_data("api1.com", 1.0)
    r2 = await fetch_data("api2.com", 1.0)
    r3 = await fetch_data("api3.com", 1.0)

    # Concurrent — all three requests run simultaneously
    # Total time: ~1 second
    results = await asyncio.gather(
        fetch_data("api1.com", 1.0),
        fetch_data("api2.com", 1.0),
        fetch_data("api3.com", 1.0),
    )

asyncio.run(main())
```

`asyncio.gather()` runs multiple coroutines concurrently. All three "sleep" at the same time, so the total wait is 1 second instead of 3.

### When to Use async

Use `asyncio` for **I/O-bound** tasks — network requests, database queries, file operations. Don't use it for **CPU-bound** tasks (heavy computation) — use `multiprocessing` for those instead.

---

## 11.4 Threading and Multiprocessing (Brief Overview)

For quick parallel execution of I/O-bound tasks without async:

```python
from concurrent.futures import ThreadPoolExecutor

def download(url):
    import time; time.sleep(0.5)
    return f"Content from {url}"

urls = [f"https://api.com/{i}" for i in range(10)]

with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(download, urls))
```

For CPU-bound tasks (computation on multiple cores):

```python
from concurrent.futures import ProcessPoolExecutor

def compute(n):
    return sum(i * i for i in range(n))

with ProcessPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(compute, [10_000_000] * 4))
```

---

## Labs

- **[Lab 11.1: Log Pipeline](./lab-01-pipeline)** — Build a generator-based log analysis pipeline
- **[Lab 11.2: Decorator Toolkit](./lab-02-decorators)** — Implement timer, retry, and caching decorators
- **[Lab 11.3: Async Fetcher](./lab-03-async)** — Fetch multiple URLs concurrently with asyncio

---

## Checklist

- [ ] Write generator functions with `yield` and explain their memory advantages
- [ ] Build generator pipelines that chain multiple stages
- [ ] Write decorators with `@functools.wraps`, including decorators with arguments
- [ ] Use `async`/`await` and `asyncio.gather` for concurrent I/O
- [ ] Explain when to use threading vs. multiprocessing vs. asyncio

---

