---
title: "Week 5: Data Structures"
sidebar:
  order: 0
---


> **Goal:** Master Python's built-in data structures — lists, dictionaries, sets, and tuples — and learn how to choose the right one for each situation.


---

## 5.1 Choosing the Right Data Structure

The data structure you choose determines how fast your program runs. This isn't an abstract concern — choosing a list where you should use a set can turn a one-second operation into a one-hour operation.

Here's the core question: **What operations do you need to perform most frequently?**

| You need to... | Use a... | Why |
|----------------|----------|-----|
| Access items by position (1st, 2nd, 3rd) | **list** | O(1) index access |
| Look up values by key | **dict** | O(1) key lookup |
| Check if something is in the collection | **set** | O(1) membership test |
| Store items that shouldn't change | **tuple** | Immutable, hashable |
| Maintain insertion order with fast lookup | **dict** | Ordered since Python 3.7 |
| Remove duplicates | **set** | Uniqueness guaranteed |

The "O(1)" notation means the operation takes constant time regardless of how many items are in the collection. "O(n)" means the time grows linearly with the collection size.

---

## 5.2 Lists

A list is an **ordered, mutable sequence**. Under the hood, it's implemented as a dynamic array — a contiguous block of memory that grows as needed.

### Creating and Accessing

```python
fruits = ["apple", "banana", "cherry"]
```

Lists are ordered, meaning items stay in the order you put them. Access by index (0-based):

```python
print(fruits[0])      # 'apple'  — first item
print(fruits[-1])     # 'cherry' — last item
print(fruits[1:3])    # ['banana', 'cherry'] — slice
```

### Modifying Lists

Because lists are mutable, you can change them in place:

```python
fruits = ["apple", "banana", "cherry"]

# Add items
fruits.append("date")             # Add to end: ['apple', 'banana', 'cherry', 'date']
fruits.insert(1, "blueberry")     # Insert at index 1: ['apple', 'blueberry', 'banana', ...]
fruits.extend(["elderberry", "fig"])  # Add multiple items to end

# Remove items
fruits.pop()                      # Remove and return LAST item
fruits.pop(0)                     # Remove and return item at index 0
fruits.remove("banana")           # Remove FIRST occurrence of value
```

**Performance matters here.** `append()` and `pop()` (without an index) are O(1) — fast. But `insert(0, ...)`, `pop(0)`, and `remove()` are O(n) — they must shift all subsequent elements. If you frequently add/remove from the front, consider `collections.deque` instead.

### Sorting

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# In-place sort (modifies the list)
numbers.sort()                     # [1, 1, 2, 3, 4, 5, 6, 9]
numbers.sort(reverse=True)         # [9, 6, 5, 4, 3, 2, 1, 1]

# Sorted copy (original unchanged)
original = [3, 1, 4, 1, 5]
ordered = sorted(original)         # original is still [3, 1, 4, 1, 5]
```

Sort with a custom key function:

```python
words = ["banana", "apple", "cherry", "date"]
words.sort(key=len)                # Sort by string length
# ['date', 'apple', 'banana', 'cherry']

# Sort complex objects
students = [
    {"name": "Alice", "grade": 92},
    {"name": "Bob", "grade": 78},
    {"name": "Charlie", "grade": 95},
]
students.sort(key=lambda s: s["grade"], reverse=True)
# Sorted by grade, highest first
```

### Unpacking

```python
first, second, third = [1, 2, 3]        # Must match length exactly
first, *rest = [1, 2, 3, 4, 5]          # first=1, rest=[2, 3, 4, 5]
first, *middle, last = [1, 2, 3, 4, 5]  # first=1, middle=[2, 3, 4], last=5
```

The `*` operator collects "the rest" into a list. Only one `*` variable is allowed.

---

## 5.3 Dictionaries

A dictionary maps **keys** to **values**. It's implemented as a hash table, giving O(1) average-case lookup. Since Python 3.7, dictionaries maintain insertion order.

### Creating and Accessing

```python
user = {"name": "Alice", "age": 30, "role": "engineer"}
```

```python
# Access by key
print(user["name"])                     # 'Alice'
# print(user["email"])                  # KeyError! Key doesn't exist

# Safe access with .get()
print(user.get("email"))                # None (no error)
print(user.get("email", "N/A"))         # 'N/A' (custom default)
```

**Always use `.get()` when the key might not exist**, unless you specifically want a `KeyError` to signal a programming bug.

### Modifying

```python
user["email"] = "alice@example.com"     # Add new key-value pair
user["age"] = 31                        # Update existing value
del user["role"]                        # Remove a key
```

### Iterating

```python
user = {"name": "Alice", "age": 30}

# Iterate over keys (default)
for key in user:
    print(key)                          # 'name', 'age'

# Iterate over values
for value in user.values():
    print(value)                        # 'Alice', 30

# Iterate over key-value pairs (most common)
for key, value in user.items():
    print(f"{key}: {value}")
```

### Merging Dictionaries

```python
defaults = {"theme": "dark", "lang": "en", "timeout": 30}
overrides = {"theme": "light", "timeout": 60}

# Spread operator merge (Python 3.5+)
config = {**defaults, **overrides}
# {'theme': 'light', 'lang': 'en', 'timeout': 60}

# Pipe operator merge (Python 3.9+)
config = defaults | overrides    # Same result
```

Later values override earlier ones for duplicate keys.

### `defaultdict` — Auto-Creating Missing Values

From the `collections` module, `defaultdict` automatically creates values for missing keys:

```python
from collections import defaultdict

# Count word frequencies
word_counts = defaultdict(int)      # Missing keys default to int() → 0
for word in "the cat sat on the mat".split():
    word_counts[word] += 1
# {'the': 2, 'cat': 1, 'sat': 1, 'on': 1, 'mat': 1}

# Group items by category
grouped = defaultdict(list)         # Missing keys default to list() → []
records = [("fruit", "apple"), ("veg", "carrot"), ("fruit", "banana")]
for category, item in records:
    grouped[category].append(item)
# {'fruit': ['apple', 'banana'], 'veg': ['carrot']}
```

### `Counter` — Specialized Counting

```python
from collections import Counter

text = "mississippi"
counts = Counter(text)
print(counts)                       # Counter({'s': 4, 'i': 4, 'p': 2, 'm': 1})
print(counts.most_common(2))        # [('s', 4), ('i', 4)]
```

---

## 5.4 Sets

A set is an **unordered collection of unique elements**. It's implemented as a hash table (like dict keys without values), giving O(1) membership testing.

```python
fruits = {"apple", "banana", "cherry"}
```

### Why Sets Matter for Performance

```python
# Checking membership in a list — O(n), checks every element
big_list = list(range(1_000_000))
999_999 in big_list                 # Slow — must scan to the end

# Checking membership in a set — O(1), constant time
big_set = set(range(1_000_000))
999_999 in big_set                  # Fast — hash table lookup
```

### Set Operations

Sets support mathematical set operations:

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b       # Union:        {1, 2, 3, 4, 5, 6}
a & b       # Intersection:  {3, 4}
a - b       # Difference:    {1, 2} (in a but not in b)
a ^ b       # Symmetric diff: {1, 2, 5, 6} (in one but not both)
```

### Deduplication

```python
raw = [1, 2, 3, 2, 1, 4, 3, 5]
unique = list(set(raw))              # [1, 2, 3, 4, 5] (order may vary)

# Preserve order while deduplicating
unique_ordered = list(dict.fromkeys(raw))  # [1, 2, 3, 4, 5] (order preserved)
```

---

## 5.5 Tuples and Named Tuples

Tuples are **immutable sequences**. Once created, they cannot be changed.

```python
point = (3, 4)
rgb = (255, 128, 0)
singleton = (42,)       # Trailing comma required for single-element tuple
```

Because tuples are immutable, they can be used as dictionary keys and set elements (unlike lists):

```python
grid = {}
grid[(0, 0)] = "origin"
grid[(1, 2)] = "point A"
```

### Named Tuples

Named tuples add field names to tuples, making code more readable:

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p = Point(3, 4)
print(p.x)       # 3 — access by name
print(p[0])      # 3 — still works as a tuple
```

---

## Labs

- **[Lab 5.1: Inventory System](./lab-01-inventory)** — Build an inventory system using dicts and sets
- **[Lab 5.2: Graph Traversal](./lab-02-graph)** — Implement BFS using deque and dict adjacency lists

---

## Checklist

- [ ] Choose the right data structure based on required operations
- [ ] Explain the performance difference between list search O(n) and set/dict search O(1)
- [ ] Use `defaultdict` and `Counter` for grouping and counting
- [ ] Perform set operations: union, intersection, difference
- [ ] Use tuples as immutable, hashable data containers

---

