# Lab 1.2: REPL Exploration

Open your terminal, activate your venv, and start `python` (or `ipython`).
Work through each exercise below by typing the code at the `>>>` prompt.

**Do not copy-paste.** Typing it yourself is part of the learning process.

---

## Exercise 1: Basic Arithmetic

Try each of these and observe the results:

```python
>>> 2 + 3
>>> 10 - 4
>>> 3 * 7
>>> 10 / 3         # What type is the result?
>>> 10 // 3        # What's different?
>>> 10 % 3         # What does % do?
>>> 2 ** 10        # What does ** do?
```

**Question:** What is the difference between `/` and `//`?

---

## Exercise 2: Variables

```python
>>> x = 10
>>> y = 3
>>> x + y
>>> x * y
>>> x / y
>>> type(x)
>>> type(x / y)
```

**Question:** `x` is an `int` and `y` is an `int`. What type is `x / y`? Why?

---

## Exercise 3: Strings

```python
>>> name = "Python"
>>> len(name)
>>> name[0]
>>> name[-1]
>>> name[0:3]
>>> name.upper()
>>> name.lower()
>>> f"Hello, {name}!"
>>> "Py" in name
>>> "py" in name
```

**Question:** Why does `"Py" in name` return `True` but `"py" in name` returns `False`?

---

## Exercise 4: Exploring Types

```python
>>> type(42)
>>> type(3.14)
>>> type("hello")
>>> type(True)
>>> type(None)
>>> type([1, 2, 3])
>>> type({"a": 1})
>>> isinstance(42, int)
>>> isinstance(42, (int, float))
```

**Question:** What does `isinstance` do differently from `type()`?

---

## Exercise 5: Getting Help

```python
>>> help(len)
>>> help(str.upper)
>>> dir(str)           # Lists ALL methods on the str type
>>> "hello".capitalize()
>>> "hello".center(20)
>>> "hello".zfill(10)
```

`dir()` and `help()` are your best friends for exploring Python.
You never need to memorize every method — just know how to find them.

---

## Bonus: Try Breaking Things

Type each of these and read the error messages carefully:

```python
>>> 1 / 0
>>> "hello" + 5
>>> int("abc")
>>> name = "Python"
>>> name[100]
```

**Learning to read error messages is one of the most important skills in programming.**
Python's error messages tell you exactly what went wrong and where. Get comfortable with them.
