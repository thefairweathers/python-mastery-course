# Python Mastery: From First Principles to AI Applications

> A structured, hands-on course for developers on Apple Silicon Macs.

---

## About This Course

This course takes you from zero to building AI-powered applications in Python. Every module is designed around a **theory → code → practice** loop: concepts are introduced in small pieces, immediately demonstrated with working code, and then reinforced through hands-on labs that you run on your own machine.

The course is written for **macOS on Apple Silicon (M-series chips)**, though the Python content itself is platform-agnostic. All examples are tested against **Python 3.13+**.

---

## How to Use This Course

Each week is a self-contained directory with:

| File | Purpose |
|------|---------|
| `README.md` | The lesson — theory, code walkthroughs, and explanations |
| `labs/` | Hands-on exercises with starter code and solutions |

**Recommended workflow:**

1. Read the week's `README.md` from top to bottom, typing out every code example yourself (don't copy-paste — the act of typing builds muscle memory)
2. After finishing the lesson, complete the labs in the `labs/` directory
3. Experiment — break things, add print statements, change values, see what happens
4. Move to the next week only when you're comfortable with the material

---

## Course Structure

| Week | Module | Topics |
|------|--------|--------|
| [Week 1](week-01/README.md) | **Environment & Tooling** | Homebrew, Python installation, virtual environments, VS Code, the REPL |
| [Week 2](week-02/README.md) | **Python Fundamentals** | Variables, types, strings, numbers, type system internals |
| [Week 3](week-03/README.md) | **Control Flow & Logic** | Conditionals, loops, comprehensions, pattern matching |
| [Week 4](week-04/README.md) | **Functions & Scope** | Definitions, arguments, closures, lambdas, first-class functions |
| [Week 5](week-05/README.md) | **Data Structures** | Lists, dicts, sets, tuples, choosing the right structure |
| [Week 6](week-06/README.md) | **Object-Oriented Programming** | Classes, inheritance, composition, dataclasses, design patterns |
| [Week 7](week-07/README.md) | **File I/O & Data Formats** | Reading/writing files, JSON, CSV, pathlib, context managers |
| [Week 8](week-08/README.md) | **Error Handling & Debugging** | Exceptions, custom errors, logging, debugging techniques |
| [Week 9](week-09/README.md) | **Modules, Packages & Project Structure** | Imports, project layout, pyproject.toml, building CLI tools |
| [Week 10](week-10/README.md) | **Testing & Code Quality** | pytest, fixtures, parametrize, coverage, linting, type checking |
| [Week 11](week-11/README.md) | **Advanced Patterns** | Generators, decorators, iterators, concurrency, async/await |
| [Week 12](week-12/README.md) | **APIs & Data Engineering** | HTTP requests, FastAPI, pandas, data visualization |
| [Week 13](week-13/README.md) | **AI & Machine Learning with Python** | NumPy, scikit-learn, Anthropic API, tool use, RAG, AI agents |

---

## Prerequisites

- An Apple Silicon Mac (M1/M2/M3/M4)
- Comfort using the Terminal (you don't need to be an expert — Week 1 covers setup)
- Curiosity and willingness to type out code by hand

---

## Quick Start

```bash
# 1. Clone this repo
git clone https://github.com/<your-username>/python-mastery.git
cd python-mastery

# 2. Follow Week 1 to set up your environment
open week-01/README.md
```

---

## Philosophy

This course follows three principles:

1. **Explain the "why" before the "how"** — Every concept starts with *why* it exists and *what problem* it solves before showing syntax.

2. **Small blocks, immediate practice** — Code is introduced in small, digestible pieces. Each block is explained line-by-line before moving to the next concept.

3. **Build real things** — Labs aren't toy exercises. They build towards real tools you'd actually use: CLI apps, APIs, data pipelines, and AI agents.

---

*Built for Python 3.13+ on Apple Silicon. Last updated: February 2026.*
