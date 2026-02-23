---
title: "Lab 6.2: Shape Library"
sidebar:
  order: 2
---

> **Download:** [`lab_02_shapes.py`](/python-mastery-course/scaffolds/week-06/lab_02_shapes.py)

```python
"""
Lab 6.2: Shape Library
=====================

Implement a shape hierarchy using ABC, inheritance, and composition.
Practice abstract methods, properties, and operator overloading.
"""

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Abstract base class for all shapes."""

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(area={self.area():.2f})"

    def __lt__(self, other: "Shape") -> bool:
        """Compare shapes by area for sorting."""
        # TODO: Implement
        pass

    def __eq__(self, other: object) -> bool:
        """Two shapes are equal if they have the same area (within tolerance)."""
        # TODO: Implement — use math.isclose
        pass


class Circle(Shape):
    """
    A circle defined by its radius.

    Properties:
    - radius: float (must be positive)
    - diameter: float (computed, read-only)
    """

    def __init__(self, radius: float):
        # TODO: Validate radius > 0, raise ValueError if not
        pass

    @property
    def radius(self) -> float:
        # TODO: Implement
        pass

    @property
    def diameter(self) -> float:
        # TODO: Implement
        pass

    def area(self) -> float:
        # TODO: Implement — π * r²
        pass

    def perimeter(self) -> float:
        # TODO: Implement — 2 * π * r
        pass


class Rectangle(Shape):
    """
    A rectangle defined by width and height.

    Properties:
    - width: float (must be positive)
    - height: float (must be positive)
    - is_square: bool (True if width == height)
    """

    def __init__(self, width: float, height: float):
        # TODO: Validate both > 0
        pass

    @property
    def is_square(self) -> bool:
        # TODO: Implement
        pass

    def area(self) -> float:
        # TODO: Implement
        pass

    def perimeter(self) -> float:
        # TODO: Implement
        pass


class Triangle(Shape):
    """
    A triangle defined by three side lengths.

    Validate that the sides form a valid triangle (triangle inequality).
    Use Heron's formula for area.
    """

    def __init__(self, a: float, b: float, c: float):
        # TODO: Validate all > 0 and triangle inequality holds
        pass

    def area(self) -> float:
        # TODO: Implement using Heron's formula
        # s = (a + b + c) / 2
        # area = sqrt(s * (s-a) * (s-b) * (s-c))
        pass

    def perimeter(self) -> float:
        # TODO: Implement
        pass


class ShapeCollection:
    """
    A collection of shapes with aggregate operations.
    Uses composition (has-a list of shapes) rather than inheritance.
    """

    def __init__(self):
        self._shapes: list[Shape] = []

    def add(self, shape: Shape) -> None:
        # TODO: Implement
        pass

    def total_area(self) -> float:
        """Return the sum of all shape areas."""
        # TODO: Implement
        pass

    def largest(self) -> Shape:
        """Return the shape with the largest area."""
        # TODO: Implement — use max() with a key
        pass

    def sorted_by_area(self) -> list[Shape]:
        """Return shapes sorted by area (smallest first)."""
        # TODO: Implement — the __lt__ method makes shapes sortable
        pass

    def __len__(self) -> int:
        return len(self._shapes)


# ============================================================
# Tests
# ============================================================

def test_circle():
    c = Circle(5)
    assert math.isclose(c.area(), 78.5398, rel_tol=1e-3)
    assert math.isclose(c.perimeter(), 31.4159, rel_tol=1e-3)
    assert c.diameter == 10
    try:
        Circle(-1)
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    print("✓ Circle passed")


def test_rectangle():
    r = Rectangle(4, 6)
    assert r.area() == 24
    assert r.perimeter() == 20
    assert r.is_square is False
    assert Rectangle(5, 5).is_square is True
    print("✓ Rectangle passed")


def test_triangle():
    t = Triangle(3, 4, 5)
    assert math.isclose(t.area(), 6.0, rel_tol=1e-3)
    assert t.perimeter() == 12
    try:
        Triangle(1, 2, 10)  # Invalid triangle
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    print("✓ Triangle passed")


def test_comparison():
    c = Circle(1)       # area ≈ 3.14
    r = Rectangle(2, 2) # area = 4
    assert c < r
    assert Circle(1) == Circle(1)
    print("✓ Shape comparison passed")


def test_collection():
    coll = ShapeCollection()
    coll.add(Circle(5))
    coll.add(Rectangle(4, 6))
    coll.add(Triangle(3, 4, 5))
    assert len(coll) == 3
    assert coll.largest().area() == max(s.area() for s in [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)])
    sorted_shapes = coll.sorted_by_area()
    assert sorted_shapes[0].area() <= sorted_shapes[1].area() <= sorted_shapes[2].area()
    print("✓ ShapeCollection passed")


if __name__ == "__main__":
    test_circle()
    test_rectangle()
    test_triangle()
    test_comparison()
    test_collection()
    print("\nAll tests passed! ✓")
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
