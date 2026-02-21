---
title: "Lab 8.1: Resilient Processor"
sidebar:
  order: 1
---

> **Download:** [`lab_01_processor.py`](/python-mastery-course/scaffolds/week-08/lab_01_processor.py)

```python
"""
Lab 8.1: Resilient Data Processor — Process records with comprehensive error handling.
TODO: Implement a processor that validates, transforms, and reports on failures.
"""
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ProcessingResult:
    total: int = 0
    succeeded: int = 0
    failed: int = 0
    errors: list = field(default_factory=list)

    def record_success(self):
        self.total += 1; self.succeeded += 1

    def record_failure(self, item, error):
        self.total += 1; self.failed += 1
        self.errors.append({"item": str(item), "error": str(error)})

class DataProcessor:
    def process_records(self, records: list[dict]) -> ProcessingResult:
        # TODO: Validate each record, transform valid ones, catch/log errors
        pass

if __name__ == "__main__":
    records = [
        {"id": 1, "name": "Alice", "value": 150},
        {"id": 2, "value": 50},          # Missing 'name'
        "not a dict",                      # Wrong type
        {"id": 4, "name": "Bob", "value": -10},  # Negative value
    ]
    processor = DataProcessor()
    result = processor.process_records(records)
    print(f"Processed: {result.succeeded}/{result.total} succeeded")
```

## Checklist

- [ ] Download the scaffold file
- [ ] Read through all the comments and understand each task
- [ ] Complete all TODO sections
- [ ] Run and verify your solution
