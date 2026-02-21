---
title: "Lab 3.1: FizzBuzz Three Ways"
sidebar:
  order: 1
---

> **Download:** [`lab_01_fizzbuzz.py`](/python-mastery-course/scaffolds/week-03/lab_01_fizzbuzz.py)

```python
"""
Lab 3.1: FizzBuzz Three Ways
=============================

FizzBuzz is a classic programming exercise:
- Print numbers 1 to 100
- For multiples of 3, print "Fizz" instead
- For multiples of 5, print "Buzz" instead
- For multiples of both 3 and 5, print "FizzBuzz"

Implement it three different ways to practice different control flow patterns.
"""


def fizzbuzz_loop(n: int) -> list[str]:
    """
    Method 1: Traditional loop with if/elif/else.

    Return a list of strings for numbers 1 through n.
    Example: fizzbuzz_loop(5) → ['1', '2', 'Fizz', '4', 'Buzz']
    """
    # TODO: Implement using a for loop with if/elif/else
    pass


def fizzbuzz_comprehension(n: int) -> list[str]:
    """
    Method 2: List comprehension with ternary expressions.

    Same output, but built in a single list comprehension.
    Hint: You can nest ternary expressions, though readability matters.
    """
    # TODO: Implement using a list comprehension
    pass


def fizzbuzz_match(n: int) -> list[str]:
    """
    Method 3: Using pattern matching on (n%3, n%5) tuples.

    Hint: match (i % 3, i % 5) gives you a tuple you can pattern-match on.
    (0, 0) means divisible by both, (0, _) means divisible by 3 only, etc.
    """
    # TODO: Implement using match/case
    pass


# ============================================================
# Tests
# ============================================================

def test_fizzbuzz(func, name):
    result = func(15)
    expected = [
        '1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8',
        'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz'
    ]
    assert result == expected, f"{name} failed!\nGot:      {result}\nExpected: {expected}"
    print(f"✓ {name} passed")


if __name__ == "__main__":
    test_fizzbuzz(fizzbuzz_loop, "fizzbuzz_loop")
    test_fizzbuzz(fizzbuzz_comprehension, "fizzbuzz_comprehension")
    test_fizzbuzz(fizzbuzz_match, "fizzbuzz_match")
    print("\nAll methods passed! ✓")
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
