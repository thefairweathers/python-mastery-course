---
title: "Lab 4.2: Data Pipeline"
sidebar:
  order: 2
---

> **Download:** [`lab_02_pipeline.py`](/python-mastery-course/scaffolds/week-04/lab_02_pipeline.py)

```python
"""
Lab 4.2: Data Pipeline
======================

Compose functions into a text processing pipeline.
Practice higher-order functions, closures, and function composition.
"""


def pipeline(*funcs):
    """
    Create a pipeline that chains functions together.

    Each function receives the output of the previous one.
    Returns a new function that applies all functions in sequence.

    Example:
        p = pipeline(str.strip, str.lower, str.title)
        p("  hello world  ") → "Hello World"

    Hint: Use functools.reduce or a loop that applies each function.
    """
    # TODO: Implement
    pass


def make_replacer(old: str, new: str):
    """
    Return a function that replaces 'old' with 'new' in a string.

    This is a closure — the returned function "remembers" old and new.

    Example:
        fix_spaces = make_replacer("  ", " ")
        fix_spaces("hello  world") → "hello world"
    """
    # TODO: Implement
    pass


def make_filter(predicate):
    """
    Return a function that filters a list using the given predicate.

    Example:
        get_positives = make_filter(lambda x: x > 0)
        get_positives([-1, 2, -3, 4]) → [2, 4]
    """
    # TODO: Implement
    pass


def make_mapper(transform):
    """
    Return a function that applies a transform to every item in a list.

    Example:
        double = make_mapper(lambda x: x * 2)
        double([1, 2, 3]) → [2, 4, 6]
    """
    # TODO: Implement
    pass


def compose(f, g):
    """
    Return a new function that computes f(g(x)).

    Mathematical function composition: (f ∘ g)(x) = f(g(x))

    Example:
        add_one = lambda x: x + 1
        double = lambda x: x * 2
        double_then_add = compose(add_one, double)
        double_then_add(5) → 11  # double(5)=10, add_one(10)=11
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

def test_pipeline():
    clean = pipeline(str.strip, str.lower)
    assert clean("  HELLO  ") == "hello"

    process = pipeline(str.strip, str.lower, str.title)
    assert process("  hello world  ") == "Hello World"

    identity = pipeline()
    assert identity("test") == "test"
    print("✓ pipeline passed")


def test_replacer():
    fix = make_replacer("world", "Python")
    assert fix("hello world") == "hello Python"

    fix_spaces = make_replacer("  ", " ")
    assert fix_spaces("too  many  spaces") == "too many spaces"
    print("✓ make_replacer passed")


def test_filter():
    get_even = make_filter(lambda x: x % 2 == 0)
    assert get_even([1, 2, 3, 4, 5, 6]) == [2, 4, 6]

    get_long = make_filter(lambda s: len(s) > 3)
    assert get_long(["hi", "hello", "hey", "howdy"]) == ["hello", "howdy"]
    print("✓ make_filter passed")


def test_mapper():
    double = make_mapper(lambda x: x * 2)
    assert double([1, 2, 3]) == [2, 4, 6]

    upper = make_mapper(str.upper)
    assert upper(["hello", "world"]) == ["HELLO", "WORLD"]
    print("✓ make_mapper passed")


def test_compose():
    add_one = lambda x: x + 1
    double = lambda x: x * 2

    double_then_add = compose(add_one, double)
    assert double_then_add(5) == 11

    add_then_double = compose(double, add_one)
    assert add_then_double(5) == 12
    print("✓ compose passed")


def test_full_pipeline():
    """Integration test: combine everything into a text processing pipeline."""
    normalize = pipeline(
        str.strip,
        str.lower,
        make_replacer("  ", " "),
        make_replacer("colour", "color"),
    )
    assert normalize("  The COLOUR  is Red  ") == "the color is red"
    print("✓ full pipeline integration test passed")


if __name__ == "__main__":
    test_pipeline()
    test_replacer()
    test_filter()
    test_mapper()
    test_compose()
    test_full_pipeline()
    print("\nAll tests passed! ✓")
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
