"""
Lab 1.1: Environment Verification
==================================

Run this script to confirm your Python environment is properly configured.
It checks everything from Week 1: Python version, virtual environment,
Apple Silicon, and installed tools.

Usage:
    cd ~/dev/python-course
    source .venv/bin/activate
    python lab_01_verify.py

Every check should show ✓. If any show ✗, review the relevant section
in Week 1's README.
"""

import sys
import platform
import os


def check(label: str, condition: bool, detail: str = ""):
    """Print a pass/fail check with optional detail."""
    status = "✓" if condition else "✗"
    msg = f"  [{status}] {label}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return condition


def main():
    print("=" * 60)
    print("PYTHON ENVIRONMENT VERIFICATION")
    print("=" * 60)
    all_passed = True

    # --- Python Version ---
    print("\n1. Python Version")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    all_passed &= check(
        "Python 3.11+",
        version >= (3, 11),
        f"You have {version_str}"
    )
    all_passed &= check(
        "Not system Python",
        "/opt/homebrew" in sys.executable or ".venv" in sys.executable,
        sys.executable
    )

    # --- Virtual Environment ---
    print("\n2. Virtual Environment")
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    all_passed &= check(
        "Virtual env active",
        in_venv,
        sys.prefix if in_venv else "Activate with: source .venv/bin/activate"
    )

    # --- Apple Silicon ---
    print("\n3. Platform")
    machine = platform.machine()
    all_passed &= check(
        "Apple Silicon (arm64)",
        machine == "arm64",
        machine
    )
    all_passed &= check(
        "macOS",
        platform.system() == "Darwin",
        platform.platform()
    )

    # --- Key tools ---
    print("\n4. Tools")

    # pip
    try:
        import pip
        all_passed &= check("pip available", True, f"v{pip.__version__}")
    except ImportError:
        all_passed &= check("pip available", False)

    # ipython (optional but recommended)
    try:
        import IPython
        check("IPython available", True, f"v{IPython.__version__}")
    except ImportError:
        check("IPython available", False, "Optional — install with: pip install ipython")

    # --- Summary ---
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL REQUIRED CHECKS PASSED ✓")
        print("You're ready for Week 2!")
    else:
        print("SOME CHECKS FAILED ✗")
        print("Review the Week 1 README for setup instructions.")
    print("=" * 60)


if __name__ == "__main__":
    main()
