# Week 1: Environment & Tooling

> **Goal:** By the end of this week, you'll have a fully configured Python development environment on your M4 Mac, understand *why* each piece matters, and be comfortable running Python code.

---

## 1.1 Why Environment Setup Matters

Before writing a single line of Python, you need to understand the terrain. Skipping environment setup is the #1 cause of frustration for new Python developers — mysterious errors, conflicting packages, and the dreaded "it works on my machine" problem all trace back to environment issues.

Here's the core problem: **your Mac already has Python installed, but you should never use it for development.** Apple ships a Python interpreter that macOS itself depends on for internal tools. If you install packages into that system Python, you can break operating system functionality. So the first thing we need to do is install our *own* Python, completely separate from Apple's.

The second problem is **dependency isolation.** Imagine you're working on two projects:
- Project A needs `requests` version 2.28
- Project B needs `requests` version 2.31

If both projects share the same Python installation, you can't have both versions at the same time. Virtual environments solve this by giving each project its own isolated set of packages.

---

## 1.2 Installing Homebrew

Homebrew is the standard package manager for macOS. It lets you install software (including Python) with simple terminal commands, and keeps everything organized under `/opt/homebrew/` on Apple Silicon Macs.

**Open Terminal** (press `Cmd + Space`, type "Terminal", press Enter) and run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

This downloads and runs the Homebrew installer. It will ask for your password (the same one you use to log into your Mac) and may take a few minutes.

After installation completes, Homebrew will print instructions to add itself to your PATH. Run the commands it shows you, which will look like:

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**What does this do?** The first line adds a command to your shell startup file (`~/.zprofile`) so that every time you open a new Terminal window, your shell knows where to find Homebrew's programs. The second line runs that same command *right now* so you don't have to restart Terminal.

Verify it worked:

```bash
brew --version
```

You should see something like `Homebrew 4.x.x`. If you get "command not found," close Terminal and reopen it, then try again.

---

## 1.3 Installing Python

Now we'll use Homebrew to install our own Python, separate from Apple's system Python.

```bash
brew install python@3.13
```

This installs the latest Python 3.13.x into Homebrew's directory. Let's verify:

```bash
python3 --version
```

You should see `Python 3.13.x`. Now let's understand what we have:

```bash
# YOUR Python (use this for development)
which python3
# Expected output: /opt/homebrew/bin/python3

# APPLE'S Python (never use this for development)
/usr/bin/python3 --version
```

The `which` command tells you *which* Python binary your shell will use when you type `python3`. It should point to Homebrew's copy, not Apple's.

### Understanding PATH

Your shell uses an environment variable called `PATH` to decide where to look for programs. `PATH` is a list of directories, separated by colons. When you type `python3`, the shell searches each directory in `PATH` from left to right and runs the first `python3` it finds.

```bash
echo $PATH
```

You'll see something like `/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:...`. Since `/opt/homebrew/bin` comes first, Homebrew's Python wins over Apple's `/usr/bin/python3`.

---

## 1.4 Virtual Environments

### The Problem

Let's say you install a package:

```bash
pip3 install requests
```

This installs `requests` into your Homebrew Python's `site-packages` directory — a shared location. Every script you run with this Python now has access to `requests`. That sounds convenient, but it creates problems:

1. **Version conflicts** — Project A needs version 2.28, Project B needs 2.31
2. **Reproducibility** — You can't tell which packages belong to which project
3. **Pollution** — Over time, you accumulate dozens of packages you don't need

### The Solution: Virtual Environments

A virtual environment (venv) is a **self-contained directory** that has its own Python binary and its own `site-packages` folder. When you activate a venv, your shell's `python` and `pip` commands point to this isolated copy instead of the system-wide one.

Here's what the directory structure looks like:

```
my-project/
├── .venv/                      ← Virtual environment (git-ignored)
│   ├── bin/                    ← Executables: python, pip, activate
│   ├── lib/python3.13/
│   │   └── site-packages/      ← Packages installed in THIS venv only
│   └── pyvenv.cfg              ← Config: points to base Python
├── src/                        ← Your source code
└── requirements.txt            ← List of dependencies
```

### Creating Your First Virtual Environment

Let's create a project directory and set up a venv:

```bash
mkdir -p ~/dev/python-course
cd ~/dev/python-course
```

The `mkdir -p` command creates the directory (and any parent directories that don't exist). `cd` changes into it.

Now create the virtual environment:

```bash
python3 -m venv .venv
```

Let's break this command apart:
- `python3` — run Python
- `-m venv` — run the built-in `venv` module as a script
- `.venv` — name of the directory to create (the leading dot makes it hidden in Finder)

### Activating the Virtual Environment

The venv exists, but it's not active yet. Activate it:

```bash
source .venv/bin/activate
```

You'll notice your terminal prompt changes — it now shows `(.venv)` at the beginning:

```
(.venv) tim@macbook python-course %
```

This visual indicator tells you which venv is active. Now let's verify that `python` and `pip` point to the venv:

```bash
which python
# Expected: /Users/<you>/dev/python-course/.venv/bin/python

which pip
# Expected: /Users/<you>/dev/python-course/.venv/bin/pip
```

Notice that once the venv is active, you can type just `python` (not `python3`) — the venv creates the alias for you.

### Installing Packages in the Venv

With the venv active, any packages you install go into the venv's `site-packages`, not the system-wide location:

```bash
pip install requests
```

Let's see what's installed:

```bash
pip list
```

You'll see `requests` and its dependencies (`certifi`, `charset-normalizer`, `idna`, `urllib3`) — but nothing else. The venv started clean.

### Saving and Restoring Dependencies

To record exactly which packages (and versions) your project needs:

```bash
pip freeze > requirements.txt
```

Open `requirements.txt` and you'll see something like:

```
certifi==2024.12.14
charset-normalizer==3.4.1
idna==3.10
requests==2.32.3
urllib3==2.3.0
```

Anyone (including future you) can recreate this exact environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Deactivating

When you're done working on this project:

```bash
deactivate
```

Your prompt returns to normal, and `python`/`pip` point back to the system-wide installation.

### The Rule

**Every project gets its own virtual environment.** Always activate the venv before working on a project, and always deactivate when you switch to a different project.

---

## 1.5 Choosing and Configuring an Editor

You need a text editor that understands Python — one that provides syntax highlighting, autocompletion, error detection, and integrated terminal access. Here are the top options:

| Editor | Strengths | Install |
|--------|-----------|---------|
| **VS Code** | Free, huge extension ecosystem, excellent Python support | `brew install --cask visual-studio-code` |
| **PyCharm CE** | Purpose-built for Python, best refactoring tools | `brew install --cask pycharm-ce` |
| **Cursor** | AI-assisted coding built in | Download from cursor.com |

We'll use **VS Code** for this course. Install it:

```bash
brew install --cask visual-studio-code
```

### Essential VS Code Extensions

Open VS Code, then install the Python extension. You can do this from the terminal:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
```

The first extension gives you Python language support (IntelliSense, linting, debugging). The second adds Black, an opinionated code formatter that automatically formats your code to a consistent style.

### Configuring VS Code for Your Project

Open your project in VS Code:

```bash
cd ~/dev/python-course
code .
```

VS Code needs to know which Python interpreter to use. Create a settings file:

```bash
mkdir -p .vscode
```

Create the file `.vscode/settings.json` with this content:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    }
}
```

Here's what each setting does:

- **`python.defaultInterpreterPath`** — Tells VS Code to use the venv's Python, not the system Python. The `${workspaceFolder}` variable expands to your project's root directory.
- **`editor.defaultFormatter`** — Uses Black to format your code.
- **`editor.formatOnSave`** — Automatically formats your code every time you save a file. This means you never have to think about formatting again.

---

## 1.6 The Python REPL

The REPL (Read-Eval-Print Loop) is Python's interactive interpreter. It reads your input, evaluates it, prints the result, and loops back for more. It's invaluable for experimentation — testing small code snippets, exploring how functions work, and debugging.

Make sure your venv is active, then start the REPL:

```bash
python
```

You'll see:

```
Python 3.13.x (main, ...) [Clang ...] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

The `>>>` is the REPL prompt. Try some expressions:

```python
>>> 2 + 2
4
```

Python evaluated `2 + 2` and printed the result. The REPL automatically prints the result of any expression, so you don't need `print()` here (though you can use it if you want).

```python
>>> name = "Python"
>>> f"Hello, {name}!"
'Hello, Python!'
```

The first line creates a variable. The second line creates an f-string (formatted string) and the REPL prints it. Notice the quotes in the output — the REPL shows the *representation* of the value, which includes quotes for strings.

```python
>>> 10 / 3
3.3333333333333335
>>> 10 // 3
3
```

`/` is true division (always returns a float). `//` is floor division (rounds down to the nearest integer).

To exit the REPL:

```python
>>> exit()
```

### Enhanced REPL: IPython

The built-in REPL is functional but basic. IPython is a much more powerful alternative with syntax highlighting, tab completion, and better error messages.

```bash
pip install ipython
ipython
```

```python
In [1]: import math

In [2]: math.pi
Out[2]: 3.141592653589793

In [3]: [x**2 for x in range(10)]
Out[3]: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

IPython numbers each input and output, making it easy to reference previous results. It also supports `?` to inspect objects:

```python
In [4]: math.sqrt?
# Shows documentation for math.sqrt
```

---

## 1.7 Running Python Files

While the REPL is great for experimentation, real programs live in `.py` files. Let's create your first one.

In your project directory, create a file called `hello.py`:

```python
# hello.py
print("Hello from a Python file!")
```

Run it from the terminal:

```bash
python hello.py
```

Output:

```
Hello from a Python file!
```

### The `if __name__ == "__main__"` Pattern

You'll see this pattern in almost every Python file. Create a file called `greeter.py`:

```python
def greet(name):
    """Return a greeting for the given name."""
    return f"Hello, {name}!"


# This block only runs when the file is executed directly
if __name__ == "__main__":
    message = greet("Tim")
    print(message)
```

Run it:

```bash
python greeter.py
# Output: Hello, Tim!
```

**Why does this pattern exist?** When Python runs a file directly, it sets a special variable `__name__` to the string `"__main__"`. But when another file *imports* this module, `__name__` is set to the module's name (e.g., `"greeter"`). This means the code inside the `if` block only runs when you execute the file directly, not when it's imported by another file.

This is crucial because it lets you write files that are both reusable modules (importable by other code) and standalone scripts (runnable from the terminal).

---

## Labs

Complete the labs in the [labs/](labs/) directory:

- **[Lab 1.1: Environment Verification](labs/lab_01_verify.py)** — Run a script that validates your entire setup
- **[Lab 1.2: REPL Exploration](labs/lab_02_repl.md)** — A set of exercises to practice in the REPL

---

## Checklist

Before moving to Week 2, confirm:

- [ ] Homebrew is installed and working (`brew --version`)
- [ ] Python 3.13+ is installed via Homebrew (`python3 --version`)
- [ ] You can create and activate a virtual environment
- [ ] VS Code is installed with the Python extension
- [ ] You can run Python files from the terminal
- [ ] You understand *why* we use virtual environments (isolation, reproducibility)
- [ ] You understand the difference between system Python and your Python

---

[Next: Week 2 — Python Fundamentals →](../week-02/README.md)
