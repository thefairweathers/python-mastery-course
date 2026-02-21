"""
Lab 13.1: Build an AI-Powered Research Agent
=============================================

Build an agent that uses Claude with tool calling to research topics.
The agent has access to a simulated knowledge base and a calculator.

This lab ties together:
- The Anthropic API (Week 13)
- JSON handling (Week 7)
- Error handling (Week 8)
- Functions as first-class objects (Week 4)
- Dictionaries (Week 5)

Prerequisites:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-key-here"

TODO: Complete the marked sections, then run the agent.
"""

import json
from typing import Callable


# ============================================================
# Step 1: Define the Knowledge Base (simulated)
# ============================================================

KNOWLEDGE_BASE = {
    "python_history": (
        "Python was created by Guido van Rossum and first released in 1991. "
        "It was named after Monty Python's Flying Circus. Python 3.0 was "
        "released in 2008 with breaking changes from Python 2."
    ),
    "python_typing": (
        "Python introduced type hints in PEP 484 (Python 3.5). They are "
        "optional annotations that don't affect runtime but help tools like "
        "mypy catch type errors. Python 3.10 added pattern matching."
    ),
    "python_performance": (
        "CPython uses a Global Interpreter Lock (GIL) that allows only one "
        "thread to execute Python bytecode at a time. For CPU-bound tasks, "
        "use multiprocessing. For I/O-bound tasks, use asyncio or threading."
    ),
    "python_packaging": (
        "Modern Python projects use pyproject.toml for configuration. "
        "Virtual environments isolate dependencies. pip installs packages "
        "from PyPI. Poetry and uv are popular dependency management tools."
    ),
}


# ============================================================
# Step 2: Define Tool Functions
# ============================================================

def search_knowledge(query: str) -> str:
    """Search the knowledge base for relevant articles."""
    query_lower = query.lower()
    results = []
    for key, content in KNOWLEDGE_BASE.items():
        if any(word in content.lower() for word in query_lower.split()):
            results.append({"topic": key, "content": content})
    if not results:
        return json.dumps({"message": "No results found", "query": query})
    return json.dumps({"results": results[:3]})


def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    import math
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
    allowed.update({"abs": abs, "round": round, "min": min, "max": max})
    try:
        result = eval(expression, {"__builtins__": {}}, allowed)
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


# Tool registry — maps tool names to functions
TOOL_FUNCTIONS: dict[str, Callable] = {
    "search_knowledge": search_knowledge,
    "calculate": calculate,
}


# ============================================================
# Step 3: Define Tool Schemas for Claude
# ============================================================

TOOLS = [
    {
        "name": "search_knowledge",
        "description": "Search the Python knowledge base for information about a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g., 'GIL threading performance')",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate (e.g., 'sqrt(16) + 2**3')",
                },
            },
            "required": ["expression"],
        },
    },
]


# ============================================================
# Step 4: TODO — Implement the Agent Loop
# ============================================================

def run_agent(user_message: str):
    """
    TODO: Implement the agent loop.

    Steps:
    1. Create an Anthropic client
    2. Initialize the messages list with the user's message
    3. In a loop:
       a. Send messages to Claude with tools
       b. Check if the response contains tool_use blocks
       c. If no tools — print the text response and break
       d. If tools — execute each one using TOOL_FUNCTIONS,
          build tool_result blocks, and continue the loop

    Refer to Section 13.5 in the Week 13 README for the pattern.

    Bonus: Add error handling for tool execution failures.
    """
    pass  # Replace with your implementation


# ============================================================
# Main — Test the Agent
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RESEARCH AGENT")
    print("=" * 60)

    queries = [
        "Tell me about Python's history and when Python 3 was released.",
        "What is the GIL and when should I use multiprocessing?",
        "What's 2^10 + sqrt(144)?",
    ]

    for query in queries:
        print(f"\n{'─' * 60}")
        print(f"User: {query}\n")
        run_agent(query)
        print()
