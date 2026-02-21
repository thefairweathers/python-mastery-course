---
title: "Lab 4.1: Memoization"
sidebar:
  order: 1
---

> **Download:** [`lab_01_memoize.py`](/python-mastery-course/scaffolds/week-04/lab_01_memoize.py)

```python
"""
Lab 4.1: Build a Memoization Decorator
=======================================

Memoization caches function results so repeated calls with the same
arguments return instantly. This lab walks you through building one
from scratch — practicing closures, decorators, and performance measurement.

Complete the TODO sections, then run the file to verify.
"""

import time
from typing import Callable


def memoize(func: Callable) -> Callable:
    """
    TODO: Implement a memoization decorator.

    Requirements:
    1. Maintain a dictionary (cache) that maps argument tuples to results
    2. Before calling the original function, check if the args are in the cache
    3. If cached, return the cached result without calling the function
    4. If not cached, call the function, store the result, and return it
    5. Expose the cache as an attribute on the wrapper: wrapper.cache = cache

    Hints:
    - Use *args as the cache key (tuples are hashable)
    - Remember to use @functools.wraps to preserve the original function's metadata
    """
    import functools
    # TODO: Implement
    pass


# ============================================================
# Test: Fibonacci Performance
# ============================================================

def fib_slow(n):
    """Fibonacci WITHOUT memoization — exponential time O(2^n)."""
    if n < 2:
        return n
    return fib_slow(n - 1) + fib_slow(n - 2)


@memoize
def fib_fast(n):
    """Fibonacci WITH memoization — linear time O(n)."""
    if n < 2:
        return n
    return fib_fast(n - 1) + fib_fast(n - 2)


def test_memoize():
    # Test correctness
    assert fib_fast(0) == 0
    assert fib_fast(1) == 1
    assert fib_fast(10) == 55
    assert fib_fast(20) == 6765
    print("✓ Correctness tests passed")

    # Test performance
    start = time.perf_counter()
    slow_result = fib_slow(30)
    slow_time = time.perf_counter() - start

    start = time.perf_counter()
    fast_result = fib_fast(100)
    fast_time = time.perf_counter() - start

    print(f"\nfib_slow(30) = {slow_result:>20,} in {slow_time:.4f}s")
    print(f"fib_fast(100) = {fast_result:>20,} in {fast_time:.6f}s")
    print(f"Cache entries: {len(fib_fast.cache)}")
    print(f"Speedup: memoized version is ~{slow_time/max(fast_time, 0.000001):,.0f}x faster")

    # Test that cache attribute exists
    assert hasattr(fib_fast, 'cache'), "Decorator must expose .cache attribute"
    print("\n✓ All tests passed!")


if __name__ == "__main__":
    test_memoize()
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
