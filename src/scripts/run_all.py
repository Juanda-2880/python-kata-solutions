"""
scripts/run_all.py
==================

End-to-end demonstration runner for ``kata_solutions``.

This script exercises all three kata modules with representative inputs,
prints formatted output, and confirms correctness of results. It is intended
as a quick smoke-test and onboarding showcase — not a replacement for the
pytest test suite.

Usage
-----
    python scripts/run_all.py

Exit Codes
----------
0   All kata demonstrations completed without assertion failures.
1   At least one result did not match the expected value.
"""

import logging
import logging.config
import sys
from pathlib import Path

# ── Resolve project root and configure path ────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"
LOG_CONFIG = PROJECT_ROOT / "config" / "logging.yaml"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

# ── Logging setup ──────────────────────────────────────────────────────────────
try:
    import yaml  # type: ignore[import]
    with open(LOG_CONFIG) as f:
        logging.config.dictConfig(yaml.safe_load(f))
except Exception:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")

logger = logging.getLogger("run_all")

# ── Import kata modules ────────────────────────────────────────────────────────
from kata_solutions.dictionary import Dictionary
from kata_solutions.nth_letter import nth_char
from kata_solutions.shopping import get_total
from kata_solutions.shopping.shopping import format_receipt

# ── Display helpers ────────────────────────────────────────────────────────────
SEPARATOR = "─" * 60


def section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def result_line(label: str, value: object, expected: object | None = None) -> bool:
    """Print a result line with optional pass/fail indicator.

    Returns True if value matches expected (or no expected given); False otherwise.
    """
    status = ""
    passed = True
    if expected is not None:
        if value == expected:
            status = "  ✓ PASS"
        else:
            status = f"  ✗ FAIL (expected {expected!r})"
            passed = False
    print(f"  {label:<30} → {value!r}{status}")
    return passed


# ══════════════════════════════════════════════════════════════════════════════
# KATA 1 — Custom Dictionary
# ══════════════════════════════════════════════════════════════════════════════

def demo_dictionary() -> bool:
    """Demonstrate the Dictionary kata with multiple usage scenarios."""
    section("KATA 1 — Custom Dictionary")
    all_passed = True

    # ── Kata specification example ─────────────────────────────────────────
    print("\n  [Kata specification example]")
    d = Dictionary()
    d.newentry("Apple", "A fruit that grows on trees")

    all_passed &= result_line(
        "d.look('Apple')",
        d.look("Apple"),
        "A fruit that grows on trees",
    )
    all_passed &= result_line(
        "d.look('Banana')",
        d.look("Banana"),
        "Can't find entry for Banana",
    )

    # ── Entry overwrite ───────────────────────────────────────────────────
    print("\n  [Entry overwrite]")
    d.newentry("Apple", "Revised: A sweet pome fruit")
    all_passed &= result_line(
        "d.look('Apple') after update",
        d.look("Apple"),
        "Revised: A sweet pome fruit",
    )

    # ── Multiple entries ──────────────────────────────────────────────────
    print("\n  [Multiple entries]")
    for word, defn in [
        ("Python", "A high-level programming language"),
        ("Kernel", "The core of an operating system"),
        ("API", "Application Programming Interface"),
    ]:
        d.newentry(word, defn)

    for word in ["Python", "Kernel", "API", "Rust"]:
        result_line(f"d.look('{word}')", d.look(word))

    # ── Utility methods ───────────────────────────────────────────────────
    print("\n  [Utility methods]")
    all_passed &= result_line("d.size()", d.size())
    all_passed &= result_line("'Python' in d", "Python" in d, True)
    all_passed &= result_line("'Rust' in d", "Rust" in d, False)

    removed = d.remove("Kernel")
    all_passed &= result_line("d.remove('Kernel')", removed, True)
    all_passed &= result_line("d.look('Kernel') after remove", d.look("Kernel"))

    logger.info("Kata 1 demonstration complete.")
    return all_passed


# ══════════════════════════════════════════════════════════════════════════════
# KATA 2 — Shopping Tax Calculator
# ══════════════════════════════════════════════════════════════════════════════

def demo_shopping() -> bool:
    """Demonstrate the shopping tax calculator with multiple scenarios."""
    section("KATA 2 — Shopping Tax Calculator")
    all_passed = True

    costs: dict[str, float | int] = {
        "socks": 5,
        "shoes": 60,
        "sweater": 30,
        "hat": 15,
        "gloves": 12,
    }

    # ── Kata specification example ─────────────────────────────────────────
    print("\n  [Kata specification example]")
    all_passed &= result_line(
        "get_total(socks+shoes, 9%)",
        get_total(costs, ["socks", "shoes"], 0.09),
        70.85,
    )

    # ── Additional scenarios ───────────────────────────────────────────────
    print("\n  [Additional scenarios]")
    all_passed &= result_line(
        "Unknown item ignored",
        get_total(costs, ["socks", "jet"], 0.0),
        5.0,
    )
    all_passed &= result_line(
        "Empty items list",
        get_total(costs, [], 0.09),
        0.0,
    )
    all_passed &= result_line(
        "Duplicate item (socks ×2)",
        get_total(costs, ["socks", "socks"], 0.0),
        10.0,
    )
    all_passed &= result_line(
        "Full basket, zero tax",
        get_total(costs, list(costs.keys()), 0.0),
        float(sum(costs.values())),
    )

    # ── Formatted receipt ──────────────────────────────────────────────────
    print("\n  [Formatted receipt output]")
    receipt = format_receipt(costs, ["socks", "shoes"], 0.09)
    for line in receipt.splitlines():
        print(f"  {line}")

    logger.info("Kata 2 demonstration complete.")
    return all_passed


# ══════════════════════════════════════════════════════════════════════════════
# KATA 3 — Nth Letter Extractor
# ══════════════════════════════════════════════════════════════════════════════

def demo_nth_letter() -> bool:
    """Demonstrate the nth letter extractor with multiple word lists."""
    section("KATA 3 — Nth Letter Extractor")
    all_passed = True

    # ── Kata specification example ─────────────────────────────────────────
    print("\n  [Kata specification example]")
    all_passed &= result_line(
        'nth_char(["yoda","best","has"])',
        nth_char(["yoda", "best", "has"]),
        "yes",
    )

    # ── Additional scenarios ───────────────────────────────────────────────
    print("\n  [Additional scenarios]")
    all_passed &= result_line("nth_char([])", nth_char([]), "")
    all_passed &= result_line('nth_char(["hello"])', nth_char(["hello"]), "h")
    all_passed &= result_line(
        'nth_char(["YODA","BEST","HAS"])',
        nth_char(["YODA", "BEST", "HAS"]),
        "YES",
    )
    all_passed &= result_line(
        'nth_char(["abc","def","ghi"])',
        nth_char(["abc", "def", "ghi"]),
        "aei",
    )

    # ── IndexError demonstration ───────────────────────────────────────────
    print("\n  [Error handling — word too short]")
    try:
        nth_char(["abc", "d"])  # "d" at index 1 but len("d") == 1
        print("  ERROR: Expected IndexError was not raised")
        all_passed = False
    except IndexError as exc:
        print(f"  ✓ IndexError raised correctly: {exc}")

    logger.info("Kata 3 demonstration complete.")
    return all_passed


# ══════════════════════════════════════════════════════════════════════════════
# Entry Point
# ══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Run all kata demonstrations and return an appropriate exit code."""
    print("\n" + "═" * 60)
    print("  python-kata-solutions — End-to-End Demonstration")
    print("  EPAM engX | Production-Grade Python Kata Solutions")
    print("═" * 60)

    results = [
        demo_dictionary(),
        demo_shopping(),
        demo_nth_letter(),
    ]

    print(f"\n{SEPARATOR}")
    all_ok = all(results)
    if all_ok:
        print("  ✓ All demonstrations passed.")
    else:
        failed = sum(1 for r in results if not r)
        print(f"  ✗ {failed} demonstration(s) had assertion failures.")
    print(SEPARATOR + "\n")

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
