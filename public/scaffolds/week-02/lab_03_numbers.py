"""
Lab 2.3: Number Cruncher
========================

Explore numeric precision, integer operations, and the Decimal module.
Complete each function according to its docstring.
"""

from decimal import Decimal, ROUND_HALF_UP


def float_trap() -> dict:
    """
    Demonstrate floating-point precision issues.

    Return a dict with:
    - 'naive_sum': the result of 0.1 + 0.2 (a float)
    - 'is_equal': whether 0.1 + 0.2 == 0.3 (a bool)
    - 'decimal_sum': the result of Decimal("0.1") + Decimal("0.2") (a Decimal)
    - 'decimal_equal': whether the Decimal sum equals Decimal("0.3") (a bool)
    """
    # TODO: Implement this function
    pass


def split_bill(total: str, num_people: int, tip_percent: str) -> dict:
    """
    Split a restaurant bill using Decimal for exact arithmetic.

    All monetary inputs are strings to avoid float imprecision.

    Return a dict with:
    - 'subtotal': the original total as Decimal
    - 'tip': tip amount, rounded to 2 decimal places
    - 'grand_total': subtotal + tip, as Decimal
    - 'per_person': grand_total / num_people, rounded to 2 decimal places
    - 'remainder': grand_total - (per_person * num_people) — the leftover cents

    Use ROUND_HALF_UP for all rounding.

    Example:
        split_bill("100.00", 3, "18") should give per_person = Decimal("39.34")
        with remainder = Decimal("-0.02") since 39.34 * 3 = 118.02 vs grand_total 118.00
    """
    # TODO: Implement this function
    pass


def base_converter(number: int) -> dict:
    """
    Convert an integer to multiple base representations.

    Return a dict with:
    - 'decimal': the number as-is (int)
    - 'binary': binary string with '0b' prefix (use bin())
    - 'octal': octal string with '0o' prefix (use oct())
    - 'hex': hex string with '0x' prefix (use hex())
    - 'num_bits': minimum number of bits needed (use int.bit_length())

    Example:
        base_converter(255) → {
            'decimal': 255,
            'binary': '0b11111111',
            'octal': '0o377',
            'hex': '0xff',
            'num_bits': 8
        }
    """
    # TODO: Implement this function
    pass


def safe_average(numbers: list) -> float | None:
    """
    Calculate the average of a list of numbers safely.

    - Return None if the list is empty
    - Handle mixed int/float lists
    - Round the result to 2 decimal places

    Example:
        safe_average([10, 20, 30]) → 20.0
        safe_average([1, 2, 3, 4, 5]) → 3.0
        safe_average([]) → None
    """
    # TODO: Implement this function
    pass


# ============================================================
# Tests — run this file to check your work
# ============================================================

def test_float_trap():
    result = float_trap()
    assert result["naive_sum"] != 0.3, "0.1 + 0.2 should NOT equal 0.3 as floats"
    assert result["is_equal"] is False, "Float comparison should be False"
    assert result["decimal_sum"] == Decimal("0.3"), "Decimal sum should be exact"
    assert result["decimal_equal"] is True, "Decimal comparison should be True"
    print("✓ float_trap passed")


def test_split_bill():
    result = split_bill("100.00", 3, "18")
    assert result["subtotal"] == Decimal("100.00")
    assert result["tip"] == Decimal("18.00")
    assert result["grand_total"] == Decimal("118.00")
    assert result["per_person"] == Decimal("39.34")
    print("✓ split_bill passed")


def test_base_converter():
    result = base_converter(255)
    assert result["binary"] == "0b11111111"
    assert result["hex"] == "0xff"
    assert result["num_bits"] == 8
    print("✓ base_converter passed")


def test_safe_average():
    assert safe_average([10, 20, 30]) == 20.0
    assert safe_average([]) is None
    assert safe_average([1, 2, 3, 4, 5]) == 3.0
    print("✓ safe_average passed")


if __name__ == "__main__":
    test_float_trap()
    test_split_bill()
    test_base_converter()
    test_safe_average()
    print("\nAll tests passed! ✓")
