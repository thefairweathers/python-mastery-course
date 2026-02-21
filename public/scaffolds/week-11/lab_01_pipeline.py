"""
Lab 11.1: Generator Pipeline — Build a log analysis pipeline.
TODO: Implement generator stages that chain together for memory-efficient processing.
"""
import re
from collections import Counter

SAMPLE_LOGS = """
2025-01-15 08:23:01 INFO  [auth] User alice logged in
2025-01-15 08:24:02 ERROR [api] Connection timeout to payment service
2025-01-15 08:24:03 WARN  [api] Retrying payment service (attempt 1)
2025-01-15 08:25:30 ERROR [auth] Failed login attempt for user admin
2025-01-15 08:26:00 INFO  [auth] User bob logged in
2025-01-15 08:27:00 ERROR [db] Connection pool exhausted
""".strip()

def generate_lines(text):
    # TODO: Yield non-empty stripped lines
    pass

def parse_entries(lines):
    # TODO: Parse each line into a dict with timestamp, level, component, message
    pass

def filter_errors(entries):
    # TODO: Yield only entries where level is ERROR or WARN
    pass

if __name__ == "__main__":
    pipeline = filter_errors(parse_entries(generate_lines(SAMPLE_LOGS)))
    for entry in pipeline:
        print(f"[{entry['level']}] {entry['component']}: {entry['message']}")
