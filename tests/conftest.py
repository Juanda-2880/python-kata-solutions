"""
tests/conftest.py
==================

Shared pytest fixtures and configuration for the kata_solutions test suite.

Fixtures defined here are automatically discovered by pytest and available to
all test modules without explicit import. Fixtures are scoped appropriately to
balance isolation and performance:

- ``function`` scope (default): fresh instance per test — used for stateful
  objects like ``Dictionary`` to prevent inter-test contamination.
- ``module`` scope: single instance per test file — used for read-only data.
- ``session`` scope: single instance per test run — used for immutable
  reference data shared across all test files.
"""

import pytest

from kata_solutions.dictionary import Dictionary
from kata_solutions.shopping import get_total  # noqa: F401 — available for injection


# ─── Dictionary Fixtures ──────────────────────────────────────────────────────

@pytest.fixture()
def empty_dictionary() -> Dictionary:
    """Return a freshly constructed, empty Dictionary instance."""
    return Dictionary()


@pytest.fixture()
def populated_dictionary() -> Dictionary:
    """Return a Dictionary pre-loaded with three well-known entries.

    Entries:
        - "Apple"  → "A fruit that grows on trees"
        - "Python" → "A high-level programming language"
        - "Cloud"  → "Distributed computing infrastructure"
    """
    d = Dictionary()
    d.newentry("Apple", "A fruit that grows on trees")
    d.newentry("Python", "A high-level programming language")
    d.newentry("Cloud", "Distributed computing infrastructure")
    return d


# ─── Shopping Fixtures ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def sample_costs() -> dict[str, float]:
    """Return a representative cost catalogue for shopping tests."""
    return {
        "socks": 5,
        "shoes": 60,
        "sweater": 30,
        "hat": 15,
        "gloves": 12,
    }


@pytest.fixture(scope="module")
def standard_tax() -> float:
    """Return the standard tax rate used in kata examples (9%)."""
    return 0.09


# ─── Nth Letter Fixtures ──────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def kata_example_words() -> list[str]:
    """Return the canonical example from the kata specification."""
    return ["yoda", "best", "has"]


@pytest.fixture(scope="module")
def kata_example_result() -> str:
    """Return the expected result for the canonical kata example."""
    return "yes"
