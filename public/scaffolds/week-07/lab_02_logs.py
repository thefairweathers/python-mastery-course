"""
Lab 7.2: Log Parser
===================

Parse and analyze a log file using file I/O and data structures.
Practice reading files, parsing text, and aggregating data.
"""

from pathlib import Path
from collections import Counter
from datetime import datetime


SAMPLE_LOG = """\
2024-01-15 08:23:01 INFO  server started on port 8080
2024-01-15 08:23:15 INFO  connected to database
2024-01-15 08:24:02 WARNING  slow query detected (1.2s)
2024-01-15 08:25:30 ERROR  failed to process request: timeout
2024-01-15 08:25:31 INFO  retrying request
2024-01-15 08:25:32 INFO  request succeeded on retry
2024-01-15 08:30:00 WARNING  memory usage at 85%
2024-01-15 08:35:22 ERROR  database connection lost
2024-01-15 08:35:23 INFO  reconnecting to database
2024-01-15 08:35:25 INFO  database reconnected
2024-01-15 09:00:00 INFO  health check passed
2024-01-15 09:15:44 ERROR  disk space low: 5% remaining
2024-01-15 09:30:00 WARNING  high CPU usage: 92%
2024-01-15 10:00:00 INFO  scheduled backup started
2024-01-15 10:05:30 INFO  backup completed successfully
"""


def parse_log_line(line: str) -> dict | None:
    """
    Parse a single log line into a structured dict.

    Expected format: "YYYY-MM-DD HH:MM:SS LEVEL  message"

    Return a dict with:
    - 'timestamp': datetime object
    - 'level': str ("INFO", "WARNING", or "ERROR")
    - 'message': str (the rest of the line)

    Return None if the line is empty or can't be parsed.

    Hint: Split carefully — the level is followed by two spaces before the message.
    """
    # TODO: Implement
    pass


def parse_log(text: str) -> list[dict]:
    """
    Parse an entire log (multi-line string) into a list of log entry dicts.
    Skip empty lines and unparseable lines.
    """
    # TODO: Implement using parse_log_line
    pass


def count_by_level(entries: list[dict]) -> dict[str, int]:
    """
    Count log entries by level.

    Return a dict like {"INFO": 9, "WARNING": 3, "ERROR": 3}

    Hint: Use collections.Counter.
    """
    # TODO: Implement
    pass


def filter_by_level(entries: list[dict], level: str) -> list[dict]:
    """
    Return only entries matching the given level.
    """
    # TODO: Implement
    pass


def errors_between(entries: list[dict], start: str, end: str) -> list[dict]:
    """
    Return ERROR entries between start and end times (inclusive).

    start and end are strings like "08:30:00" (time only, same date assumed).

    Hint: Compare datetime.time() objects.
    """
    # TODO: Implement
    pass


def write_report(entries: list[dict], output_path: Path) -> None:
    """
    Write a summary report to a file.

    The report should contain:
    - Total entries count
    - Count per level
    - List of all ERROR messages with timestamps
    - Time range (first to last entry)

    Use pathlib and the 'with' statement.
    """
    # TODO: Implement
    pass


# ============================================================
# Tests
# ============================================================

def test_parse_line():
    entry = parse_log_line("2024-01-15 08:23:01 INFO  server started on port 8080")
    assert entry is not None
    assert entry["level"] == "INFO"
    assert entry["message"] == "server started on port 8080"
    assert isinstance(entry["timestamp"], datetime)
    assert parse_log_line("") is None
    print("✓ parse_log_line passed")


def test_parse_log():
    entries = parse_log(SAMPLE_LOG)
    assert len(entries) == 15
    print("✓ parse_log passed")


def test_count_by_level():
    entries = parse_log(SAMPLE_LOG)
    counts = count_by_level(entries)
    assert counts["INFO"] == 9
    assert counts["WARNING"] == 3
    assert counts["ERROR"] == 3
    print("✓ count_by_level passed")


def test_filter():
    entries = parse_log(SAMPLE_LOG)
    errors = filter_by_level(entries, "ERROR")
    assert len(errors) == 3
    assert all(e["level"] == "ERROR" for e in errors)
    print("✓ filter_by_level passed")


def test_errors_between():
    entries = parse_log(SAMPLE_LOG)
    errors = errors_between(entries, "08:30:00", "09:30:00")
    assert len(errors) == 2  # database connection lost + disk space low
    print("✓ errors_between passed")


def test_write_report(tmp_path=None):
    entries = parse_log(SAMPLE_LOG)
    output = Path("/tmp/test_log_report.txt")
    write_report(entries, output)
    assert output.exists()
    content = output.read_text()
    assert "Total entries: 15" in content
    assert "ERROR" in content
    output.unlink()
    print("✓ write_report passed")


if __name__ == "__main__":
    test_parse_line()
    test_parse_log()
    test_count_by_level()
    test_filter()
    test_errors_between()
    test_write_report()
    print("\nAll tests passed! ✓")
