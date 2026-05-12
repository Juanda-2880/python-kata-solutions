"""
kata_solutions.shopping.shopping
=================================

Kata 2 — How Much Will You Spend?

Calculates the total purchase cost of a list of items given a price catalogue
and a tax rate. Items absent from the catalogue are silently skipped, allowing
callers to pass partial or mixed shopping lists without raising errors.

Algorithm
---------
1. Iterate over each item in the purchase list.
2. Sum costs only for items present in the ``costs`` catalogue.
3. Apply the tax multiplier: ``total = subtotal * (1 + tax_rate)``.
4. Round the result to two decimal places for currency precision.

Design Notes
------------
- The function is intentionally stateless: all inputs are parameters, all
  output is the return value. No global state, no side effects.
- ``Decimal`` is intentionally avoided here to keep the solution idiomatic
  for competitive kata grading where ``round()`` is the conventional tool.
  For production financial systems, use the ``decimal`` standard-library module
  with ``ROUND_HALF_UP`` to avoid floating-point accumulation errors.
- Unknown items are skipped (not penalised), as per kata specification.

Usage
-----
>>> costs = {"socks": 5, "shoes": 60, "sweater": 30}
>>> get_total(costs, ["socks", "shoes"], 0.09)
70.85
>>> get_total(costs, ["socks", "hat"], 0.10)  # "hat" is ignored
5.5
>>> get_total(costs, [], 0.09)
0.0
"""

import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)

# Type alias for the costs catalogue
CostCatalogue = dict[str, float | int]


def get_total(
    costs: CostCatalogue,
    items: Sequence[str],
    tax_rate: float,
) -> float:
    """Calculate the total purchase cost of a list of items, including tax.

    Iterates over ``items``, sums the prices of those present in ``costs``,
    and returns the total after applying the given tax multiplier. Items not
    found in ``costs`` are silently ignored, per kata specification.

    Parameters
    ----------
    costs : dict[str, float | int]
        A mapping of item name → unit price. Prices must be non-negative
        numeric values. The catalogue is not mutated during execution.
    items : Sequence[str]
        An ordered list of item names to purchase. Duplicates are allowed
        and each occurrence is priced individually (e.g. buying two socks
        costs 2 × the socks price). Items absent from ``costs`` are skipped.
    tax_rate : float
        The fractional tax rate to apply after summing costs. A value of
        ``0.09`` represents 9% tax. Must be >= 0.

    Returns
    -------
    float
        The total purchase amount rounded to two decimal places, inclusive
        of the specified tax rate. Returns ``0.0`` if ``items`` is empty or
        no items are found in the catalogue.

    Raises
    ------
    TypeError
        If ``costs`` is not a ``dict``, ``items`` is not a sequence, or
        ``tax_rate`` is not a numeric type.
    ValueError
        If ``tax_rate`` is negative.

    Examples
    --------
    >>> costs = {"socks": 5, "shoes": 60, "sweater": 30}
    >>> get_total(costs, ["socks", "shoes"], 0.09)
    70.85

    >>> get_total(costs, ["socks", "hat"], 0.10)
    5.5

    >>> get_total({}, ["socks"], 0.05)
    0.0

    >>> get_total(costs, ["socks", "socks"], 0.00)
    10.0
    """
    # ── Input validation ─────────────────────────────────────────────────────
    if not isinstance(costs, dict):
        raise TypeError(f"'costs' must be a dict, got {type(costs).__name__!r}")
    if not isinstance(items, (list, tuple)):
        raise TypeError(
            f"'items' must be a list or tuple, got {type(items).__name__!r}"
        )
    if not isinstance(tax_rate, (int, float)):
        raise TypeError(
            f"'tax_rate' must be numeric (int or float), got {type(tax_rate).__name__!r}"
        )
    if tax_rate < 0:
        raise ValueError(f"'tax_rate' must be >= 0, got {tax_rate!r}")

    # ── Core computation ──────────────────────────────────────────────────────
    subtotal: float = 0.0
    skipped: list[str] = []

    for item in items:
        if item in costs:
            price = costs[item]
            subtotal += price
            logger.debug("Added item %r at price %.2f; running subtotal: %.2f", item, price, subtotal)
        else:
            skipped.append(item)
            logger.debug("Item %r not found in catalogue — skipped.", item)

    if skipped:
        logger.info("Skipped %d item(s) not in catalogue: %s", len(skipped), skipped)

    total = round(subtotal * (1 + tax_rate), 2)
    logger.debug(
        "Subtotal: %.2f | Tax rate: %.4f | Total: %.2f", subtotal, tax_rate, total
    )
    return total


def format_receipt(
    costs: CostCatalogue,
    items: Sequence[str],
    tax_rate: float,
    currency_symbol: str = "$",
) -> str:
    """Generate a formatted receipt string for a purchase.

    A helper function that wraps ``get_total`` and presents the result in a
    human-readable receipt format. Intended for display and logging purposes.

    Parameters
    ----------
    costs : CostCatalogue
        Item price catalogue (same as ``get_total``).
    items : Sequence[str]
        Items purchased (same as ``get_total``).
    tax_rate : float
        Tax rate as a fraction (same as ``get_total``).
    currency_symbol : str, optional
        Prefix symbol for monetary values, by default ``"$"``.

    Returns
    -------
    str
        A multi-line formatted receipt string.

    Examples
    --------
    >>> costs = {"socks": 5, "shoes": 60}
    >>> print(format_receipt(costs, ["socks", "shoes"], 0.09))
    ── Receipt ──────────────────
      socks          $  5.00
      shoes          $ 60.00
    ────────────────────────────
      Subtotal       $ 65.00
      Tax (9.00%)    $  5.85
      TOTAL          $ 70.85
    ────────────────────────────
    """
    lines: list[str] = ["── Receipt ──────────────────"]
    subtotal: float = 0.0

    for item in items:
        if item in costs:
            price = float(costs[item])
            subtotal += price
            lines.append(f"  {item:<14} {currency_symbol} {price:>6.2f}")

    tax_amount = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax_amount, 2)
    tax_pct = tax_rate * 100

    lines.append("────────────────────────────")
    lines.append(f"  {'Subtotal':<14} {currency_symbol} {subtotal:>6.2f}")
    lines.append(f"  {f'Tax ({tax_pct:.2f}%)':<14} {currency_symbol} {tax_amount:>6.2f}")
    lines.append(f"  {'TOTAL':<14} {currency_symbol} {total:>6.2f}")
    lines.append("────────────────────────────")

    return "\n".join(lines)
