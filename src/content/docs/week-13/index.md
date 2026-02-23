---
title: "Week 13: AI & Machine Learning with Python"
sidebar:
  order: 0
---


> **Goal:** Apply everything you've learned to build AI-powered applications — from NumPy fundamentals through calling Claude's API, implementing tool use, RAG, and building MCP servers.


---

## 13.1 The AI/ML Python Ecosystem

Python dominates AI/ML because of its library ecosystem. Here's how the pieces fit together:

| Layer | Library | What It Does |
|-------|---------|-------------|
| **Math Foundation** | NumPy | Fast array math (vectors, matrices) |
| **Data Manipulation** | pandas | Tabular data processing |
| **Classical ML** | scikit-learn | Traditional algorithms (regression, classification, clustering) |
| **Deep Learning** | PyTorch | Neural networks, GPU acceleration |
| **NLP / Transformers** | Hugging Face | Pre-trained models (BERT, GPT, etc.) |
| **AI APIs** | `anthropic` SDK | Cloud-hosted LLMs (Claude) |
| **AI Agents** | FastMCP | Tool use via Model Context Protocol |

This week focuses on the practical layers: NumPy for understanding how ML works under the hood, scikit-learn for classical ML, and the Anthropic SDK for building AI-powered applications.

---

## 13.2 NumPy — The Foundation

NumPy provides n-dimensional arrays and vectorized operations that run in compiled C, making them orders of magnitude faster than pure Python loops.

```bash
pip install numpy
```

### Why NumPy Matters

```python
import numpy as np
import time

# Pure Python — slow
data = list(range(1_000_000))
start = time.perf_counter()
result_py = [x * 2 for x in data]
print(f"Python list: {time.perf_counter() - start:.4f}s")

# NumPy — fast (typically 10-100x faster)
arr = np.arange(1_000_000)
start = time.perf_counter()
result_np = arr * 2
print(f"NumPy array: {time.perf_counter() - start:.4f}s")
```

NumPy is fast because:
1. Data is stored in contiguous memory (cache-friendly)
2. Operations are implemented in C, not Python
3. Operations apply to entire arrays at once (vectorization)

### Creating Arrays

```python
a = np.array([1, 2, 3, 4, 5])             # From a list
b = np.zeros((3, 4))                       # 3×4 matrix of zeros
c = np.ones((2, 3))                        # 2×3 matrix of ones
d = np.arange(0, 10, 0.5)                  # Like range() but for floats
e = np.linspace(0, 1, 5)                   # 5 evenly spaced values from 0 to 1
f = np.random.randn(1000)                  # 1000 samples from standard normal distribution
```

### Vectorized Operations

Operations apply element-wise to entire arrays — no loops needed:

```python
prices = np.array([10.0, 20.0, 30.0, 40.0])
tax_rate = 0.13

# These operate on ALL elements at once
totals = prices * (1 + tax_rate)           # [11.3, 22.6, 33.9, 45.2]
discounted = prices * 0.9                  # [9.0, 18.0, 27.0, 36.0]
expensive = prices[prices > 25]            # [30.0, 40.0] — boolean indexing
```

### Statistical Operations

```python
data = np.random.randn(10000)              # 10,000 random values

print(f"Mean:   {data.mean():.4f}")        # ~0.0
print(f"Std:    {data.std():.4f}")         # ~1.0
print(f"Min:    {data.min():.4f}")
print(f"Max:    {data.max():.4f}")
print(f"Median: {np.median(data):.4f}")
```

---

## 13.3 scikit-learn — Machine Learning

scikit-learn provides a consistent interface for machine learning algorithms. Every algorithm follows the same pattern: `.fit()` to train, `.predict()` to make predictions.

```bash
pip install scikit-learn
```

### Example: Predicting Values with a Random Forest

```python
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
```

**Step 1: Generate sample data.** In a real project, you'd load this from a CSV or database.

```python
X, y = make_regression(n_samples=1000, n_features=5, noise=10, random_state=42)
# X = input features (1000 samples, 5 features each)
# y = target values we want to predict
```

**Step 2: Split into training and test sets.** We hold back 20% of the data to evaluate how well the model generalizes to unseen data.

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

**Step 3: Create and train the model.**

```python
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)     # Train on the training data
```

**Step 4: Evaluate.**

```python
y_pred = model.predict(X_test)  # Predict on unseen test data

rmse = mean_squared_error(y_test, y_pred, squared=False)
r2 = r2_score(y_test, y_pred)
print(f"RMSE: {rmse:.2f}")      # Lower is better
print(f"R² Score: {r2:.4f}")    # 1.0 is perfect, 0.0 is random
```

**Step 5: Understand what the model learned.**

```python
for i, importance in enumerate(model.feature_importances_):
    print(f"Feature {i}: {importance:.4f}")
```

Feature importance tells you which input features had the most influence on predictions — invaluable for understanding your data.

---

## 13.4 The Anthropic API — Working with Claude

The Anthropic Python SDK lets you programmatically interact with Claude.

```bash
pip install anthropic
```

Set your API key as an environment variable:

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Basic Completion

```python
import anthropic

client = anthropic.Anthropic()  # Reads ANTHROPIC_API_KEY from environment

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain Python generators in 3 sentences."}
    ],
)

print(message.content[0].text)
```

Let's break this apart:
- **`client = anthropic.Anthropic()`** creates a client that handles authentication and HTTP requests.
- **`model`** specifies which Claude model to use.
- **`max_tokens`** limits the response length.
- **`messages`** is a list of conversation turns, each with a `role` ("user" or "assistant") and `content`.
- The response's text is in `message.content[0].text`.

### Multi-Turn Conversations

To maintain context across multiple exchanges, include the full conversation history:

```python
conversation = []

def chat(user_message: str) -> str:
    """Send a message and get a response, maintaining conversation history."""
    conversation.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="You are a Python tutor. Be concise and use code examples.",
        messages=conversation,
    )

    assistant_message = response.content[0].text
    conversation.append({"role": "assistant", "content": assistant_message})
    return assistant_message

# Multi-turn conversation — each message has full context
print(chat("What is a decorator?"))
print(chat("Show me a practical example."))
print(chat("How do I add arguments to that decorator?"))
```

### Streaming Responses

For long responses, streaming shows output token by token instead of waiting for the entire response:

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a Python quicksort implementation."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
print()
```

### Structured Output with Claude

Claude can extract structured data from unstructured text:

```python
import json

invoice_text = """
Invoice #2024-0142
Date: March 15, 2025
Vendor: CloudTech Solutions
Items:
- Server hosting (3 months): $2,400.00
- SSL Certificate: $150.00
Total: $2,550.00
"""

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="Extract invoice data as JSON. Return ONLY valid JSON, no other text.",
    messages=[{"role": "user", "content": f"Extract:\n{invoice_text}"}],
)

invoice_data = json.loads(response.content[0].text)
print(json.dumps(invoice_data, indent=2))
```

---

## 13.5 Tool Use — AI Agents That Take Action

Claude can use **tools** (functions you define) to interact with external systems. You describe available tools, Claude decides when and how to use them, and you execute the tool calls and feed results back.

### Defining Tools

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
            },
            "required": ["city"],
        },
    },
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression"},
            },
            "required": ["expression"],
        },
    },
]
```

### Executing Tool Calls

```python
def execute_tool(name: str, input_data: dict) -> str:
    """Execute a tool and return the result as a string."""
    if name == "get_weather":
        # In production, call a real weather API
        return json.dumps({"city": input_data["city"], "temp": 22, "condition": "Sunny"})
    elif name == "calculate":
        import math
        result = eval(input_data["expression"], {"__builtins__": {}}, vars(math))
        return json.dumps({"result": result})
    return json.dumps({"error": f"Unknown tool: {name}"})
```

### The Agent Loop

The agent loop sends a message to Claude, checks if it wants to use tools, executes them, feeds results back, and repeats until Claude gives a final answer:

```python
def run_agent(user_message: str):
    """Run an agent that can use tools to answer questions."""
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages,
        )

        # Check if Claude wants to use any tools
        tool_blocks = [b for b in response.content if b.type == "tool_use"]

        if not tool_blocks:
            # No tools — Claude has a final answer
            for block in response.content:
                if block.type == "text":
                    print(block.text)
            break

        # Execute each tool Claude requested
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in tool_blocks:
            print(f"  [Calling {block.name}({block.input})]")
            result = execute_tool(block.name, block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

        messages.append({"role": "user", "content": tool_results})
        # Loop continues — Claude processes tool results and may call more tools

run_agent("What's the weather in Tokyo, and what's sqrt(144)?")
```

This pattern is the foundation of AI agents — Claude reasons about what tools to use, you execute them, and Claude incorporates the results into its response.

---

## 13.6 RAG — Retrieval-Augmented Generation

RAG enhances Claude's responses with your own data. The pattern:
1. **Embed** your documents into vectors (numerical representations)
2. **Search** for documents relevant to the user's question
3. **Augment** Claude's prompt with the relevant documents
4. **Generate** a response grounded in your data

```python
def rag_query(question: str, documents: list[str]) -> str:
    """Answer a question using relevant documents as context."""

    # Step 1: Find relevant documents (simplified — use embeddings in production)
    relevant = [doc for doc in documents if any(
        word in doc.lower() for word in question.lower().split()
    )]

    # Step 2: Build the augmented prompt
    context = "\n\n".join(relevant[:3])

    # Step 3: Send to Claude with context
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system="Answer based ONLY on the provided context. If the context doesn't contain the answer, say so.",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}",
        }],
    )

    return response.content[0].text
```

In production, you'd use proper vector embeddings (from the Anthropic or OpenAI embeddings API) and a vector database (Pinecone, ChromaDB, or pgvector) for efficient similarity search.

---

## 13.7 MCP Servers — Exposing Tools to AI

The **Model Context Protocol** (MCP) standardizes how AI models interact with external tools and data. Building an MCP server lets Claude (and other AI models) access your data through a standardized interface.

```bash
pip install fastmcp
```

```python
from fastmcp import FastMCP

mcp = FastMCP("My Data Server")

@mcp.tool()
def search_notes(query: str) -> str:
    """Search notes by keyword."""
    # Your database query here
    results = [{"title": "Python Tips", "body": "Use generators for large data..."}]
    return str(results)

@mcp.tool()
def create_note(title: str, body: str) -> str:
    """Create a new note."""
    # Your database insert here
    return f"Created note: {title}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8000)
```

This server exposes `search_notes` and `create_note` as tools that Claude can call through the MCP protocol. It's the same tool-use pattern from Section 13.5, but standardized so any MCP-compatible client can use it.

---

## Labs

- **[Lab 13.1: AI Agent](./lab-01-agent)** — Build an AI-powered agent with tool use and the Anthropic SDK

---

## Capstone Project Ideas

You now have all the skills to build substantial applications. Here are four project ideas that combine everything from the course:

1. **Personal Finance Analyzer** — Read bank CSV exports, categorize transactions with pattern matching, generate monthly reports with pandas, and visualize trends. *(File I/O, pandas, matplotlib, dataclasses)*

2. **REST API with Database** — Build a task management API with FastAPI, SQLite persistence, and a comprehensive pytest test suite. *(FastAPI, SQL, OOP, error handling, testing)*

3. **AI Document Q&A** — Ingest documents, create embeddings, store in a vector database, and build a chat interface that answers questions about your documents. *(Anthropic API, RAG, file processing, async I/O)*

4. **MCP Data Server** — Build an MCP server that exposes a real data source (database, API, or file system) as tools for Claude. *(FastMCP, async Python, API design, tool architecture)*

---

## Checklist

- [ ] Create and manipulate NumPy arrays; explain why vectorization is fast
- [ ] Train and evaluate a scikit-learn model with train/test split
- [ ] Call the Anthropic API for completions, streaming, and multi-turn conversations
- [ ] Implement tool use (function calling) with Claude
- [ ] Explain the RAG pattern and build a simple implementation
- [ ] Build an MCP server that exposes tools via FastMCP

---

## What's Next

Congratulations — you've completed the course. From here:

- **Deepen your AI skills:** Explore the [Anthropic documentation](https://docs.anthropic.com) for advanced features like vision, PDF processing, and extended thinking.
- **Learn a web framework:** Django or Flask for full web applications.
- **Explore data science:** matplotlib, seaborn, and Jupyter notebooks for exploratory analysis.
- **Contribute to open source:** Find a Python project on GitHub and submit a pull request.

The most important thing now is to **build**. Pick a project that matters to you and start writing code. The skills you've built in this course are your foundation — the real learning happens when you apply them to problems you care about.

---

