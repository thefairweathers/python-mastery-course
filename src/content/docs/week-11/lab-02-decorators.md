---
title: "Lab 11.2: Decorator Toolkit"
sidebar:
  order: 2
---

> **Download:** [`lab_02_decorators.py`](/python-mastery-course/scaffolds/week-11/lab_02_decorators.py)

```python
"""
Lab 11.2: Decorator Toolkit
============================

Implement timer, retry, and caching decorators.
Practice closures, *args/**kwargs forwarding, and functools.wraps.
"""

import functools
import time
import random


def timer(func):
    """
    Decorator that prints how long the function took to execute.

    Print: "{func_name} took {elapsed:.4f}s"

    Use time.perf_counter() for precise timing.
    Don't forget @functools.wraps(func) to preserve metadata.
    """
    # TODO: Implement
    pass


def retry(max_attempts: int = 3, delay: float = 0.1):
    """
    Decorator FACTORY that retries a function on exception.

    - Retry up to max_attempts times
    - Wait 'delay' seconds between attempts (use time.sleep)
    - If all attempts fail, re-raise the last exception
    - Print "Attempt {n}/{max_attempts} failed: {error}" on each failure

    Usage:
        @retry(max_attempts=3, delay=0.5)
        def flaky_function():
            ...

    Hint: This is a THREE-level nested function:
        retry(args) -> decorator(func) -> wrapper(*args, **kwargs)
    """
    # TODO: Implement
    pass


def cache(max_size: int = 128):
    """
    Decorator FACTORY that caches function results (LRU-style).

    - Cache based on all positional and keyword arguments
    - If cache exceeds max_size, remove the oldest entry
    - Expose cache stats via wrapper.cache_info() returning a dict:
      {"hits": int, "misses": int, "size": int, "max_size": int}
    - Expose wrapper.cache_clear() to reset the cache

    Hint: Use a dict for the cache. For ordered eviction,
    you can use dict's insertion order (Python 3.7+) and pop the
    first key when full.
    """
    # TODO: Implement
    pass


def validate_types(**type_specs):
    """
    Decorator FACTORY that validates argument types at runtime.

    Usage:
        @validate_types(name=str, age=int)
        def greet(name, age):
            return f"{name} is {age}"

        greet("Alice", 30)     # OK
        greet("Alice", "old")  # Raises TypeError

    Raise TypeError with message:
        "Argument '{name}' must be {expected_type.__name__}, got {actual_type.__name__}"
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

def test_timer(capsys=None):
    @timer
    def slow_add(a, b):
        time.sleep(0.05)
        return a + b

    result = slow_add(1, 2)
    assert result == 3
    assert slow_add.__name__ == "slow_add"  # functools.wraps preserves name
    print("✓ timer passed")


def test_retry():
    call_count = 0

    @retry(max_attempts=3, delay=0.01)
    def flaky():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Connection refused")
        return "success"

    result = flaky()
    assert result == "success"
    assert call_count == 3
    print("✓ retry passed (succeeded on attempt 3)")

    # Test that it raises after all attempts fail
    @retry(max_attempts=2, delay=0.01)
    def always_fails():
        raise ValueError("always fails")

    try:
        always_fails()
        assert False, "Should have raised"
    except ValueError:
        pass
    print("✓ retry raises after max attempts")


def test_cache():
    call_count = 0

    @cache(max_size=3)
    def expensive(n):
        nonlocal call_count
        call_count += 1
        return n * n

    assert expensive(2) == 4
    assert expensive(2) == 4   # cached
    assert call_count == 1     # only called once
    print("✓ cache hit works")

    expensive(3)
    expensive(4)
    info = expensive.cache_info()
    assert info["hits"] >= 1
    assert info["size"] <= 3
    print(f"  Cache info: {info}")
    print("✓ cache works")

    expensive.cache_clear()
    assert expensive.cache_info()["size"] == 0
    print("✓ cache_clear works")


def test_validate_types():
    @validate_types(name=str, age=int)
    def greet(name, age):
        return f"{name} is {age}"

    assert greet("Alice", 30) == "Alice is 30"

    try:
        greet("Alice", "thirty")
        assert False, "Should raise TypeError"
    except TypeError as e:
        assert "age" in str(e)
    print("✓ validate_types passed")


if __name__ == "__main__":
    test_timer()
    test_retry()
    test_cache()
    test_validate_types()
    print("\nAll tests passed! ✓")
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
