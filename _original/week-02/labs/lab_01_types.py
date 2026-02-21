"""
Lab 2.1: Type Explorer
======================

Investigate Python's type system and how objects work in memory.
Run this file and study the output carefully.

Then complete the exercises at the bottom marked with TODO.
"""


def part1_identity_vs_equality():
    """Understand the difference between 'is' and '=='."""
    print("PART 1: Identity vs. Equality")
    print("-" * 40)

    # Python caches small integers (-5 to 256) for performance.
    # This means two variables with the same small integer value
    # will point to the SAME object in memory.
    a = 256
    b = 256
    print(f"a = {a}, b = {b}")
    print(f"  a == b : {a == b}")    # True — same value
    print(f"  a is b : {a is b}")    # True — same object (cached)
    print(f"  id(a)  : {id(a)}")
    print(f"  id(b)  : {id(b)}")

    # But integers above 256 are NOT cached
    a = 257
    b = 257
    print(f"\na = {a}, b = {b}")
    print(f"  a == b : {a == b}")    # True — same value
    print(f"  a is b : {a is b}")    # Usually False — different objects!

    # Lists are NEVER cached — each [] creates a new object
    x = [1, 2, 3]
    y = [1, 2, 3]
    z = x                            # z points to the SAME object as x
    print(f"\nx = [1,2,3], y = [1,2,3], z = x")
    print(f"  x == y : {x == y}")    # True — same contents
    print(f"  x is y : {x is y}")    # False — different objects
    print(f"  x is z : {x is z}")    # True — same object


def part2_mutation_through_references():
    """See how shared references cause unexpected mutations."""
    print("\n\nPART 2: Mutation Through References")
    print("-" * 40)

    original = [1, 2, 3]
    alias = original           # alias points to the SAME list
    copy = original.copy()     # copy is a NEW list with same values

    print(f"Before: original={original}, alias={alias}, copy={copy}")

    alias.append(4)            # Modifying through alias...

    print(f"After:  original={original}, alias={alias}, copy={copy}")
    print("  original changed too! Because alias IS original.")
    print("  copy is unaffected because it's a separate object.")


def part3_float_precision():
    """Explore floating-point precision limitations."""
    print("\n\nPART 3: Float Precision")
    print("-" * 40)

    from math import isclose
    from decimal import Decimal

    print(f"0.1 + 0.2 = {0.1 + 0.2}")
    print(f"0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")
    print(f"isclose(0.1 + 0.2, 0.3)? {isclose(0.1 + 0.2, 0.3)}")

    # Decimal gives exact decimal arithmetic
    d = Decimal("0.1") + Decimal("0.2")
    print(f"\nDecimal('0.1') + Decimal('0.2') = {d}")
    print(f"Decimal result == Decimal('0.3')? {d == Decimal('0.3')}")


# ============================================================
# EXERCISES: Complete the TODO sections below
# ============================================================

def exercise1():
    """
    TODO: Without running this code first, predict the output
    of each print statement. Then run it to check.

    Write your predictions as comments next to each print.
    """
    a = "hello"
    b = "hello"
    c = "hell" + "o"

    print(a == b)       # Predict:
    print(a is b)       # Predict:
    print(a == c)       # Predict:
    print(a is c)       # Predict: (this one is tricky!)


def exercise2():
    """
    TODO: Create a variable called 'big_number' with the value
    one billion (1,000,000,000). Use underscores for readability.
    Then print:
      - Its type
      - The number of digits (hint: convert to string first)
      - Whether it's an instance of int
    """
    pass  # Replace with your code


def exercise3():
    """
    TODO: Demonstrate that bool is a subclass of int.
    Show that True + True + True equals 3.
    Then use this fact to count how many numbers in the list
    below are greater than 50.
    """
    numbers = [23, 67, 45, 89, 12, 56, 78, 34, 91, 50]
    pass  # Replace with your code


if __name__ == "__main__":
    part1_identity_vs_equality()
    part2_mutation_through_references()
    part3_float_precision()

    print("\n\n" + "=" * 50)
    print("EXERCISES")
    print("=" * 50)
    exercise1()
    exercise2()
    exercise3()
