---
title: "Week 6: Object-Oriented Programming"
sidebar:
  order: 0
---


> **Goal:** Understand classes, objects, inheritance, and composition. Learn to model real-world concepts as Python objects and apply core design patterns.


---

## 6.1 What OOP Solves

So far, you've been writing functions that operate on data structures — lists of dicts, nested tuples, etc. This works fine for small programs, but as complexity grows, you start running into problems:

- **Data and logic are separate.** A `user` dict floats around, and various functions scattered across your code know how to manipulate it. If the dict's structure changes, you must find and update every function.
- **No guardrails.** Nothing prevents someone from setting `user["age"] = "banana"` — there's no validation or encapsulation.
- **Hard to extend.** If you need a "premium user" with extra features, you end up duplicating code.

**Classes** solve these problems by bundling data and the operations on that data into a single unit. A class is a blueprint; an object (instance) is a specific realization of that blueprint.

---

## 6.2 Defining a Class

Let's build a `BankAccount` class step by step, explaining each piece as we add it.

### Step 1: The Bare Minimum

```python
class BankAccount:
    pass
```

This creates a class that does nothing. The `pass` keyword is a placeholder for an empty block. You can create instances:

```python
account = BankAccount()
print(type(account))     # <class '__main__.BankAccount'>
```

### Step 2: The Constructor (`__init__`)

The `__init__` method is called automatically when you create a new instance. It initializes the object's data:

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance
```

**`self`** is the first parameter of every instance method. It refers to the specific instance being created or operated on. When you call `BankAccount("Alice", 1000)`, Python creates a new object and passes it as `self` to `__init__`.

**`self.owner = owner`** creates an **instance variable** — data that belongs to *this specific* account, not to all accounts.

**`self._balance`** — the leading underscore is a **convention** meaning "this is internal; don't access it directly from outside the class." Python doesn't enforce this (you *can* access `account._balance`), but it signals intent.

```python
alice = BankAccount("Alice", 1000)
bob = BankAccount("Bob", 500)

print(alice.owner)     # 'Alice'
print(bob.owner)       # 'Bob' — each instance has its own data
```

### Step 3: Adding Methods

Methods are functions that operate on the instance:

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance

    def deposit(self, amount: float) -> None:
        """Add money to the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: float) -> None:
        """Remove money from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def get_balance(self) -> float:
        """Return the current balance."""
        return self._balance
```

The methods validate inputs before modifying state. This is **encapsulation** — the class controls how its data is accessed and modified, preventing invalid states.

```python
account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.get_balance())    # 1500
account.withdraw(200)
print(account.get_balance())    # 1300
# account.withdraw(5000)        # ValueError: Insufficient funds
```

### Step 4: Properties

Instead of `get_balance()`, Python offers **properties** — methods that look like attribute access:

```python
class BankAccount:
    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        """Read-only access to balance."""
        return self._balance

    # ... deposit, withdraw methods ...
```

Now you access balance like an attribute, but it's actually calling the property method:

```python
print(account.balance)          # 1300 — reads like an attribute
# account.balance = 9999        # AttributeError — it's read-only
```

### Step 5: Dunder Methods (Magic Methods)

Dunder (double-underscore) methods let your class integrate with Python's built-in operations:

```python
class BankAccount:
    # ... __init__, deposit, withdraw, balance property ...

    def __repr__(self) -> str:
        """Unambiguous representation (for developers/debugging)."""
        return f"BankAccount(owner={self.owner!r}, balance={self._balance})"

    def __str__(self) -> str:
        """Human-readable representation."""
        return f"{self.owner}'s account: ${self._balance:,.2f}"

    def __eq__(self, other) -> bool:
        """Enable == comparison between accounts."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner and self._balance == other._balance
```

- **`__repr__`** is called by `repr()` and shown in the REPL. It should be unambiguous — ideally, valid Python that recreates the object.
- **`__str__`** is called by `str()` and `print()`. It should be human-friendly.
- **`__eq__`** enables `==` comparison. Returning `NotImplemented` tells Python to try the other operand's `__eq__` instead.

```python
account = BankAccount("Alice", 1000)
print(repr(account))    # BankAccount(owner='Alice', balance=1000)
print(account)           # Alice's account: $1,000.00
```

---

## 6.3 Class Variables vs. Instance Variables

```python
class BankAccount:
    bank_name = "Python National Bank"   # Class variable — shared by ALL instances
    _total_accounts = 0

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner               # Instance variable — unique to each instance
        self._balance = balance
        BankAccount._total_accounts += 1

    @classmethod
    def get_total_accounts(cls) -> int:
        """Class method — operates on the class, not an instance."""
        return cls._total_accounts
```

- **Class variables** are defined directly in the class body (not inside `__init__`). They're shared by all instances and accessed via `ClassName.variable`.
- **`@classmethod`** receives the class as its first argument (`cls`), not an instance. Use it for factory methods or operations that affect the class as a whole.
- **`@staticmethod`** receives neither the instance nor the class. It's just a regular function that's logically grouped with the class.

---

## 6.4 Inheritance

Inheritance lets you create a new class based on an existing one. The new class (child/subclass) inherits all methods and attributes from the parent (superclass) and can add or override them.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class — cannot be instantiated directly."""

    @abstractmethod
    def area(self) -> float:
        """Every shape must implement area()."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Every shape must implement perimeter()."""
        ...

    def describe(self) -> str:
        """Concrete method — inherited by all subclasses."""
        return f"{self.__class__.__name__}: area={self.area():.2f}"
```

`ABC` (Abstract Base Class) means you can't create a `Shape()` directly — you must create a subclass that implements all `@abstractmethod` methods:

```python
class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        from math import pi
        return pi * self.radius ** 2

    def perimeter(self) -> float:
        from math import pi
        return 2 * pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
```

**Polymorphism** — different classes responding to the same interface:

```python
shapes = [Circle(5), Rectangle(4, 6), Circle(3)]
for shape in shapes:
    print(shape.describe())    # Works for any Shape subclass
```

---

## 6.5 Composition Over Inheritance

Inheritance models "is-a" relationships (a Circle *is a* Shape). **Composition** models "has-a" relationships and is often more flexible:

```python
class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def start(self):
        return f"Engine ({self.horsepower}hp) started"

class Car:
    def __init__(self, make: str, engine: Engine):
        self.make = make
        self.engine = engine    # Car HAS-AN Engine (composition)

    def start(self):
        return f"{self.make}: {self.engine.start()}"
```

**Rule of thumb:** Use inheritance when there's a genuine "is-a" relationship and shared behavior. Use composition when you want to combine capabilities from different sources.

---

## 6.6 Dataclasses

For classes that are primarily data holders, `@dataclass` eliminates boilerplate:

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    email: str
    age: int
    tags: list[str] = field(default_factory=list)

    def is_adult(self) -> bool:
        return self.age >= 18
```

This automatically generates `__init__`, `__repr__`, and `__eq__` methods. The `field(default_factory=list)` handles the mutable default argument pattern safely.

```python
user = User("Alice", "alice@example.com", 30)
print(user)              # User(name='Alice', email='alice@example.com', age=30, tags=[])
print(user == User("Alice", "alice@example.com", 30))  # True
```

---

## Labs

- **[Lab 6.1: Event System](./lab-01-events)** — Build a publish/subscribe event system using the Observer pattern
- **[Lab 6.2: Shape Library](./lab-02-shapes)** — Implement a shape hierarchy with ABC, inheritance, and composition

---

## Checklist

- [ ] Define classes with `__init__`, instance methods, and properties
- [ ] Explain the difference between class variables and instance variables
- [ ] Implement `__repr__`, `__str__`, and `__eq__` dunder methods
- [ ] Use inheritance with ABC for shared interfaces
- [ ] Apply composition ("has-a") vs. inheritance ("is-a") appropriately
- [ ] Use `@dataclass` to eliminate boilerplate for data-centric classes

---

