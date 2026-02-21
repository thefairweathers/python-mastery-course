---
title: "Lab 7.1: Config Manager"
sidebar:
  order: 1
---

> **Download:** [`lab_01_config.py`](/python-mastery-course/scaffolds/week-07/lab_01_config.py)

```python
"""
Lab 7.1: Configuration Manager — Layered config: defaults → file → env vars.
TODO: Implement ConfigManager with get/set using dot notation (e.g., 'database.host').
"""
import json, os
from pathlib import Path

class ConfigManager:
    DEFAULT_CONFIG = {"app_name": "MyApp", "debug": False, "database": {"host": "localhost", "port": 5432}}

    def __init__(self, config_path="config.json"):
        self.path = Path(config_path)
        self._config = json.loads(json.dumps(self.DEFAULT_CONFIG))
        # TODO: Load from file if exists, then apply env overrides

    def get(self, key: str, default=None):
        # TODO: Support dot notation like 'database.host'
        pass

    def set(self, key: str, value):
        # TODO: Support dot notation
        pass

if __name__ == "__main__":
    config = ConfigManager()
    print(config.get("app_name"))
    print(config.get("database.host"))
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
