---
title: "Lab 11.3: Async Fetcher"
sidebar:
  order: 3
---

> **Download:** [`lab_03_async.py`](/python-mastery-course/scaffolds/week-11/lab_03_async.py)

```python
"""
Lab 11.3: Async Fetcher
=======================

Fetch multiple URLs concurrently with asyncio.
Practice async/await, aiohttp, and concurrent task management.

Install dependency: pip install aiohttp
"""

import asyncio
import time


# ============================================================
# Part 1: Async Basics (no external dependencies)
# ============================================================

async def delay(seconds: float, label: str) -> str:
    """
    Simulate an async operation that takes 'seconds' to complete.

    - Print "{label} starting..."
    - await asyncio.sleep(seconds)
    - Print "{label} done after {seconds}s"
    - Return the label

    This is the simplest possible async function.
    """
    # TODO: Implement
    pass


async def run_sequential(tasks: list[tuple[float, str]]) -> list[str]:
    """
    Run delay tasks one after another (sequentially).

    tasks is a list of (seconds, label) tuples.
    Return a list of labels in completion order.

    This should take roughly sum(seconds) total time.
    """
    # TODO: Implement
    pass


async def run_concurrent(tasks: list[tuple[float, str]]) -> list[str]:
    """
    Run delay tasks concurrently using asyncio.gather().

    tasks is a list of (seconds, label) tuples.
    Return a list of labels in the order passed (gather preserves order).

    This should take roughly max(seconds) total time.
    """
    # TODO: Implement using asyncio.gather()
    pass


# ============================================================
# Part 2: URL Fetcher (requires aiohttp)
# ============================================================

async def fetch_url(url: str, session=None) -> dict:
    """
    Fetch a single URL and return a result dict.

    Return:
    {
        "url": the URL,
        "status": HTTP status code (int),
        "size": length of response body (int),
        "elapsed": time taken in seconds (float)
    }

    On error, return:
    {
        "url": the URL,
        "status": 0,
        "error": str(exception),
        "elapsed": time taken (float)
    }

    If session is None, create a temporary one.

    Hint: Use aiohttp.ClientSession for HTTP requests.
    """
    # TODO: Implement
    pass


async def fetch_all(urls: list[str], max_concurrent: int = 5) -> list[dict]:
    """
    Fetch all URLs concurrently with a concurrency limit.

    Use asyncio.Semaphore(max_concurrent) to limit how many
    requests run at the same time.

    Return a list of result dicts from fetch_url.
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

async def test_sequential():
    tasks = [(0.1, "A"), (0.1, "B"), (0.1, "C")]
    start = time.perf_counter()
    results = await run_sequential(tasks)
    elapsed = time.perf_counter() - start
    assert results == ["A", "B", "C"]
    assert elapsed >= 0.3, f"Sequential should take >= 0.3s, took {elapsed:.2f}s"
    print(f"✓ run_sequential passed ({elapsed:.2f}s)")


async def test_concurrent():
    tasks = [(0.1, "A"), (0.1, "B"), (0.1, "C")]
    start = time.perf_counter()
    results = await run_concurrent(tasks)
    elapsed = time.perf_counter() - start
    assert results == ["A", "B", "C"]
    assert elapsed < 0.25, f"Concurrent should take < 0.25s, took {elapsed:.2f}s"
    print(f"✓ run_concurrent passed ({elapsed:.2f}s) — {0.3/elapsed:.1f}x speedup!")


async def test_fetch():
    """Test URL fetching (requires internet)."""
    try:
        import aiohttp
    except ImportError:
        print("⊘ Skipping fetch tests (pip install aiohttp to enable)")
        return

    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/404",
    ]

    start = time.perf_counter()
    results = await fetch_all(urls, max_concurrent=3)
    elapsed = time.perf_counter() - start

    assert len(results) == 3
    for r in results:
        assert "url" in r
        print(f"  {r['url']}: status={r.get('status', 'error')}")

    print(f"✓ fetch_all passed ({elapsed:.2f}s for {len(urls)} URLs)")


async def main():
    await test_sequential()
    await test_concurrent()
    await test_fetch()
    print("\nAll tests passed! ✓")


if __name__ == "__main__":
    asyncio.run(main())
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
