---
title: "Week 2: Python Fundamentals"
sidebar:
  order: 0
---


> **Goal:** Understand how Python's type system works, master strings and numbers, and learn how Python manages objects in memory.


---

## 2.1 How Python Executes Your Code

Before diving into syntax, it helps to understand what happens when you run `python my_script.py`. This knowledge will make error messages more meaningful and help you reason about performance later.

When Python processes your `.py` file, it goes through three stages:

1. **Parsing** — Python reads your source code and converts it into an Abstract Syntax Tree (AST), which is a structured representation of your code's logic. If you have a syntax error (like a missing colon), this is where Python catches it — *before* running anything.

2. **Compilation** — The AST is compiled into **bytecode**, a set of low-level instructions that Python's virtual machine understands. This bytecode is cached in `__pycache__/` directories as `.pyc` files, so Python doesn't have to recompile unchanged files every time.

3. **Execution** — The CPython virtual machine reads the bytecode instructions one by one and executes them. This is where your program actually runs.

The key insight: Python is not purely interpreted (reading source code line-by-line) nor traditionally compiled (producing machine code). It sits in between — compiling to bytecode, then interpreting that bytecode.

You can actually see the bytecode for any function:

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

You don't need to understand bytecode to write Python, but knowing it exists helps explain why Python behaves the way it does.

---

## 2.2 Variables Are References, Not Boxes

This is one of the most important mental models in Python, and it's different from many other languages.

In languages like C, a variable is a named location in memory — a "box" that holds a value. In Python, **a variable is a name tag that points to an object.** The object exists independently, and multiple names can point to the same object.

Let's see this in action:

```python
x = 42
```

This does two things:
1. Creates an integer object with value `42` somewhere in memory
2. Makes the name `x` point to that object

Now:

```python
y = x
```

This does **not** copy the value 42. It makes `y` point to the **exact same object** that `x` points to. Both names reference the same integer `42` in memory.

```python
x = 99
```

This creates a **new** integer object `99` and makes `x` point to it. `y` still points to the original `42` — it was never changed.

```python
print(x)  # 99
print(y)  # 42
```

You can verify that two variables point to the same object using the `id()` function, which returns an object's memory address:

```python
a = [1, 2, 3]
b = a

print(id(a))        # e.g., 4512345678
print(id(b))        # Same number — same object!
print(a is b)       # True — 'is' checks identity (same object)
```

This becomes critical with mutable objects like lists, as we'll see shortly.

---

## 2.3 Core Data Types

Python has a small set of built-in types that cover the vast majority of your needs. Let's go through each one in detail.

### Integers

Python integers have **arbitrary precision** — they can be as large as your memory allows. This is unusual; most languages have fixed-size integers that overflow at some limit (like 2,147,483,647 for a 32-bit int).

```python
small = 42
negative = -17
big = 10 ** 100        # A "googol" — 1 followed by 100 zeros
```

That last line would cause an overflow in C, Java, or JavaScript. Python handles it natively:

```python
print(big)
# 10000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
print(len(str(big)))   # 101 digits
```

You can write integers in different bases using prefixes:

```python
decimal = 255          # Base 10 (default)
binary = 0b11111111    # Base 2 — the 0b prefix means binary
octal = 0o377          # Base 8 — the 0o prefix means octal
hexadecimal = 0xFF     # Base 16 — the 0x prefix means hex

# These are all the same value
print(decimal == binary == octal == hexadecimal)  # True
```

For readability, you can use underscores as digit separators:

```python
population = 8_100_000_000    # Much easier to read than 8100000000
budget = 1_500_000
```

### Floats

Floats represent decimal numbers using IEEE 754 double-precision (64-bit) format. This gives you roughly 15-17 significant digits of precision.

```python
pi = 3.14159
temperature = -40.0
avogadro = 6.022e23        # Scientific notation: 6.022 × 10²³
tiny = 1.6e-19             # 1.6 × 10⁻¹⁹
```

**The float precision gotcha.** This surprises almost everyone the first time:

```python
print(0.1 + 0.2)           # 0.30000000000000004
print(0.1 + 0.2 == 0.3)    # False!
```

This is not a Python bug — it's a fundamental limitation of how computers represent decimal fractions in binary. The number 0.1 cannot be represented exactly in binary floating-point, just as 1/3 cannot be represented exactly in decimal (0.333...).

**How to handle it:**

```python
# Method 1: Use math.isclose for comparisons
from math import isclose
print(isclose(0.1 + 0.2, 0.3))    # True

# Method 2: Use Decimal for exact decimal arithmetic (financial calculations)
from decimal import Decimal
price = Decimal("19.99")
tax = Decimal("0.13")
total = price * (1 + tax)
print(total)                        # 22.5887 (exact)
```

### Booleans

Booleans represent truth values. There are exactly two: `True` and `False`.

```python
is_active = True
is_deleted = False
```

An important Python detail: `bool` is a **subclass of `int`**. `True` is literally equal to `1` and `False` is equal to `0`:

```python
print(True + True)     # 2
print(True * 10)       # 10
print(False + 1)       # 1
```

This isn't a quirk — it's a deliberate design choice that makes counting boolean conditions easy:

```python
scores = [85, 42, 91, 67, 78, 95, 55]
passing = sum(score >= 70 for score in scores)   # Counts True values
print(f"{passing} students passed")               # 4 students passed
```

### None

`None` is Python's null value — it represents the absence of a value. There is exactly one `None` object in any Python program.

```python
result = None
```

Always use `is` (not `==`) to check for `None`:

```python
# Correct
if result is None:
    print("No result yet")

# Also correct
if result is not None:
    print(f"Got result: {result}")

# Avoid this — it works but is considered bad style
if result == None:    # Don't do this
    pass
```

**Why `is` instead of `==`?** Because `==` calls an object's `__eq__` method, which could be overridden to return `True` for non-None values. The `is` operator checks object identity — whether two variables point to the exact same object — which is both more correct and faster.

### Truthiness and Falsiness

Every Python value can be evaluated as a boolean. This is called "truthiness." The following values are **falsy** (evaluate to `False`):

```python
# All of these are falsy
bool(None)       # False
bool(False)      # False
bool(0)          # False
bool(0.0)        # False
bool("")         # False (empty string)
bool([])         # False (empty list)
bool({})         # False (empty dict)
bool(set())      # False (empty set)
```

**Everything else is truthy.** This means you can use any value in a conditional:

```python
name = ""
if name:                  # Falsy — empty string
    print(f"Hello, {name}")
else:
    print("No name provided")

items = [1, 2, 3]
if items:                 # Truthy — non-empty list
    print(f"Processing {len(items)} items")
```

This is a core Python pattern. You'll use it constantly.

---

## 2.4 Strings In Depth

Strings are one of the types you'll work with most. They're **immutable sequences of Unicode characters** — "immutable" means once a string is created, it cannot be changed. Every string operation that appears to modify a string actually creates a new one.

### Creating Strings

```python
single = 'Hello'              # Single quotes
double = "Hello"              # Double quotes — exactly equivalent
multiline = """This string
spans multiple
lines"""                      # Triple quotes for multi-line

raw = r"C:\new\folder"       # Raw string — backslashes are literal, not escapes
# Without r: "C:\new\folder" would interpret \n as a newline
```

Single and double quotes are interchangeable. The convention is to pick one style and be consistent. Double quotes are slightly more common in the Python community.

### Indexing and Slicing

Strings are sequences, which means you can access individual characters by position (indexing) or extract substrings (slicing).

```python
s = "Hello, World!"
```

**Indexing** uses square brackets with a single number. Positions start at 0:

```
 H  e  l  l  o  ,     W  o  r  l  d  !
 0  1  2  3  4  5  6  7  8  9  10 11 12
-13-12-11-10 -9 -8 -7 -6 -5 -4 -3 -2 -1
```

```python
print(s[0])      # 'H' — first character
print(s[7])      # 'W' — eighth character (0-based!)
print(s[-1])     # '!' — last character
print(s[-6])     # 'W' — sixth from the end
```

**Slicing** extracts a range using `[start:stop:step]`. The start is **inclusive** and the stop is **exclusive**:

```python
print(s[0:5])    # 'Hello'     — characters 0, 1, 2, 3, 4 (not 5)
print(s[7:12])   # 'World'     — characters 7, 8, 9, 10, 11
print(s[:5])     # 'Hello'     — omitting start means "from the beginning"
print(s[7:])     # 'World!'    — omitting stop means "to the end"
print(s[::2])    # 'Hlo ol!'   — every 2nd character
print(s[::-1])   # '!dlroW ,olleH' — reversed (step of -1)
```

The reason `stop` is exclusive is so that `s[:n] + s[n:]` always equals the original string — the split point doesn't duplicate a character.

### Essential String Methods

Remember: strings are immutable, so every method returns a **new** string.

```python
text = "  Hello, World!  "

# Whitespace handling
text.strip()                    # 'Hello, World!'   — removes leading/trailing whitespace
text.lstrip()                   # 'Hello, World!  ' — left strip only
text.rstrip()                   # '  Hello, World!' — right strip only

# Case conversion
"hello".upper()                 # 'HELLO'
"HELLO".lower()                 # 'hello'
"hello world".title()           # 'Hello World'
"hello world".capitalize()      # 'Hello world' (only first character)

# Searching
"Hello, World!".find("World")   # 7 (index where it starts)
"Hello, World!".find("xyz")     # -1 (not found)
"Hello, World!".count("l")      # 3

# Testing
"hello123".isalnum()            # True (all alphanumeric)
"hello".isalpha()               # True (all alphabetic)
"12345".isdigit()               # True (all digits)
"Hello".startswith("He")        # True
"Hello".endswith("lo")          # True

# Splitting and joining
"a,b,c,d".split(",")           # ['a', 'b', 'c', 'd']
"hello world".split()           # ['hello', 'world'] — splits on whitespace by default
", ".join(["a", "b", "c"])      # 'a, b, c'

# Replacing
"Hello, World!".replace("World", "Python")   # 'Hello, Python!'
```

### F-Strings (Formatted String Literals)

F-strings are the modern, preferred way to build strings from variables and expressions. Prefix the string with `f` and put expressions inside `{}`:

```python
name = "Tim"
age = 35

# Basic interpolation
greeting = f"Hello, {name}!"
info = f"{name} is {age} years old"

# Expressions inside braces
future = f"In 10 years, {name} will be {age + 10}"

# Format specifiers (after a colon inside the braces)
pi = 3.14159265358979
print(f"Pi: {pi:.2f}")              # 'Pi: 3.14'        — 2 decimal places
print(f"Pi: {pi:.5f}")              # 'Pi: 3.14159'     — 5 decimal places

price = 1299.99
print(f"Price: ${price:,.2f}")      # 'Price: $1,299.99' — comma separator

# Alignment
print(f"{'left':<20}|")             # 'left                |' — left-aligned, 20 chars wide
print(f"{'center':^20}|")           # '       center       |' — centered
print(f"{'right':>20}|")            # '               right|' — right-aligned

# Padding with zeros
order_num = 42
print(f"Order #{order_num:05d}")    # 'Order #00042' — zero-padded to 5 digits
```

F-strings can contain any valid Python expression, but keep them readable. If the expression is complex, compute it on a separate line first.

---

## 2.5 Type Conversion

Python won't implicitly convert between most types (unlike JavaScript, where `"5" + 3` gives `"53"`). You need to convert explicitly:

```python
# String → Integer
age = int("42")              # 42
# int("hello")               # ValueError — not a valid integer

# String → Float
price = float("19.99")      # 19.99

# Number → String
label = str(42)              # '42'
label = str(3.14)            # '3.14'

# Float → Integer (truncates toward zero — does NOT round)
print(int(3.9))              # 3
print(int(-3.9))             # -3

# Integer → Float
print(float(42))             # 42.0

# Anything → Boolean
print(bool(0))               # False
print(bool(42))              # True
print(bool(""))              # False
print(bool("hello"))         # True
```

The `int()` function truncates — it chops off the decimal part. If you want rounding:

```python
print(round(3.5))            # 4
print(round(3.49))           # 3
print(round(3.14159, 2))     # 3.14 — round to 2 decimal places
```

---

## 2.6 Operators and Expressions

### Arithmetic Operators

```python
10 + 3       # 13    — addition
10 - 3       # 7     — subtraction
10 * 3       # 30    — multiplication
10 / 3       # 3.33  — true division (always returns float)
10 // 3      # 3     — floor division (rounds DOWN, returns int if both operands are int)
10 % 3       # 1     — modulo (remainder after division)
10 ** 3      # 1000  — exponentiation
```

The **floor division** (`//`) rounds toward negative infinity, not toward zero. This matters for negative numbers:

```python
print(7 // 2)        # 3
print(-7 // 2)       # -4  (not -3! rounds toward negative infinity)
```

### Augmented Assignment

Instead of writing `x = x + 5`, you can write:

```python
x = 10
x += 5       # x = x + 5  → 15
x -= 3       # x = x - 3  → 12
x *= 2       # x = x * 2  → 24
x //= 5      # x = x // 5 → 4
x **= 3      # x = x ** 3 → 64
```

### Comparison and Chaining

```python
10 == 10     # True   — equal
10 != 5      # True   — not equal
10 > 5       # True   — greater than
10 >= 10     # True   — greater than or equal
5 < 10       # True   — less than
5 <= 5       # True   — less than or equal
```

Python supports **chained comparisons**, which is rare among programming languages and very readable:

```python
x = 15
print(10 < x < 20)          # True — is x between 10 and 20?
print(1 <= x <= 100)         # True — is x between 1 and 100?
print(0 < x < 10 < 20)      # False — x is not less than 10
```

This is equivalent to `(10 < x) and (x < 20)` but more readable and evaluates `x` only once.

### Logical Operators

```python
True and False     # False
True or False      # True
not True           # False
```

**Short-circuit evaluation:** Python evaluates `and`/`or` lazily and returns the value that determined the result (not necessarily `True` or `False`):

```python
print(0 and "hello")          # 0       — 0 is falsy, so returns 0 without evaluating "hello"
print(1 and "hello")          # 'hello' — 1 is truthy, so evaluates and returns "hello"
print("" or "default")        # 'default' — "" is falsy, so evaluates and returns "default"
print("value" or "default")   # 'value'   — "value" is truthy, returns it immediately
```

This enables a common pattern for default values:

```python
username = None
display_name = username or "Anonymous"
print(display_name)     # 'Anonymous'
```

---

## Labs

Complete the labs in the `labs/` directory:

- **[Lab 2.1: Type Explorer](./lab-01-types)** — Investigate Python's type system and object identity
- **[Lab 2.2: String Processor](./lab-02-strings)** — Build a text analysis tool using string methods
- **[Lab 2.3: Number Cruncher](./lab-03-numbers)** — Explore numeric precision and the Decimal module

---

## Checklist

Before moving to Week 3, confirm you understand:

- [ ] Variables are names (references), not boxes — assignment doesn't copy
- [ ] The difference between `==` (equality) and `is` (identity)
- [ ] Why `0.1 + 0.2 != 0.3` and how to handle it
- [ ] How truthiness works — which values are falsy
- [ ] String indexing, slicing, and the most common methods
- [ ] F-string formatting with alignment and number formatting
- [ ] Short-circuit evaluation in `and`/`or`

---

