"""
Lab 2.2: String Processor
=========================

Build a text analysis tool using the string methods from this week's lesson.
Complete each function according to its docstring.
"""


def analyze_text(text: str) -> dict:
    """
    Analyze a block of text and return a dictionary with:
    - 'char_count': total number of characters
    - 'word_count': total number of words
    - 'line_count': total number of lines
    - 'unique_words': number of unique words (case-insensitive)
    - 'avg_word_length': average length of words (rounded to 1 decimal)
    - 'longest_word': the longest word in the text

    Hints:
    - Use .split() for words and .splitlines() for lines
    - Use a set to find unique words
    - Strip punctuation from words before measuring length
    """
    # TODO: Implement this function
    pass


def format_table(headers: list, rows: list) -> str:
    """
    Create a formatted text table using f-string alignment.

    Example:
        headers = ["Name", "Age", "City"]
        rows = [["Alice", "30", "Toronto"], ["Bob", "25", "Vancouver"]]

    Should produce:
        Name           Age            City
        ─────────────  ─────────────  ─────────────
        Alice          30             Toronto
        Bob            25             Vancouver

    Hints:
    - Use f-strings with :<15 for left-alignment in a 15-char column
    - Use "─" * 13 for the separator line
    """
    # TODO: Implement this function
    pass


def caesar_cipher(text: str, shift: int) -> str:
    """
    Implement a Caesar cipher — shift each letter by 'shift' positions.

    Rules:
    - Only shift letters (a-z, A-Z); leave numbers/punctuation unchanged
    - Preserve case: 'A' shifted by 1 → 'B', 'z' shifted by 1 → 'a'
    - Handle wrapping: 'z' shifted by 1 → 'a'

    Example:
        caesar_cipher("Hello, World!", 3) → "Khoor, Zruog!"

    Hints:
    - ord('a') gives the Unicode code point of 'a'
    - chr(97) gives the character for code point 97 → 'a'
    - Use modulo (%) for wrapping
    """
    # TODO: Implement this function
    pass


# ============================================================
# Tests — run this file to check your work
# ============================================================

def test_analyze():
    text = """Python is great.
Python is powerful.
Learning Python is fun."""

    result = analyze_text(text)
    assert result["word_count"] == 9, f"Expected 9 words, got {result['word_count']}"
    assert result["line_count"] == 3, f"Expected 3 lines, got {result['line_count']}"
    assert result["unique_words"] == 6, f"Expected 6 unique, got {result['unique_words']}"
    print("✓ analyze_text passed")


def test_format():
    result = format_table(
        ["Name", "Score"],
        [["Alice", "95"], ["Bob", "87"]]
    )
    assert "Alice" in result
    assert "Bob" in result
    print("✓ format_table passed")


def test_cipher():
    assert caesar_cipher("Hello, World!", 3) == "Khoor, Zruog!"
    assert caesar_cipher("abc", 1) == "bcd"
    assert caesar_cipher("xyz", 3) == "abc"
    assert caesar_cipher("Khoor, Zruog!", -3) == "Hello, World!"
    print("✓ caesar_cipher passed")


if __name__ == "__main__":
    test_analyze()
    test_format()
    test_cipher()
    print("\nAll tests passed! ✓")
