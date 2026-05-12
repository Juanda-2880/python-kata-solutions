"""
tests/test_shopping.py
=======================

Unit tests for ``kata_solutions.shopping.get_total`` and ``format_receipt``.

Test Strategy
-------------
- Validates the exact kata example output first.
- Tests unknown items being skipped without error.
- Validates rounding to exactly two decimal places.
- Tests zero tax, 100% tax, and high-precision tax rates.
- Tests empty items list and empty catalogue.
- Tests duplicate items being counted individually.
- Tests type validation for all three parameters.
- Tests ``format_receipt`` output structure.
"""

import pytest

from kata_solutions.shopping import get_total
from kata_solutions.shopping.shopping import format_receipt


# ─── Kata Specification ───────────────────────────────────────────────────────

class TestKataSpecification:
    """Validates the exact behaviour specified in the kata description."""

    def test_kata_canonical_example(
        self,
        sample_costs: dict[str, float],
        standard_tax: float,
    ) -> None:
        """Replicates the kata's exact example: socks(5) + shoes(60) × 1.09 = 70.85."""
        result = get_total(sample_costs, ["socks", "shoes"], standard_tax)
        assert result == 70.85

    def test_unknown_item_is_ignored(
        self, sample_costs: dict[str, float]
    ) -> None:
        """Items absent from the catalogue contribute 0 to the total."""
        result = get_total(sample_costs, ["socks", "unicorn"], 0.0)
        assert result == 5.0

    def test_all_items_unknown_returns_zero(
        self, sample_costs: dict[str, float]
    ) -> None:
        """All unknown items → total is 0.0 (no catalogue match)."""
        result = get_total(sample_costs, ["dragon", "unicorn"], 0.09)
        assert result == 0.0

    def test_output_rounded_to_two_decimal_places(self) -> None:
        """Result has exactly two decimal places for currency formatting."""
        costs = {"item": 1}
        result = get_total(costs, ["item"], 0.333)
        # 1 × 1.333 = 1.333 → rounded to 1.33
        assert result == 1.33


# ─── Tax Behaviour ────────────────────────────────────────────────────────────

class TestTaxBehaviour:
    """Tests focused on tax rate edge cases and precision."""

    @pytest.mark.unit
    def test_zero_tax_returns_subtotal(self, sample_costs: dict[str, float]) -> None:
        """Zero tax rate returns the exact subtotal with no markup."""
        result = get_total(sample_costs, ["socks", "shoes"], 0.0)
        assert result == 65.0

    @pytest.mark.unit
    def test_100_percent_tax_doubles_subtotal(self) -> None:
        """100% tax doubles the subtotal exactly."""
        costs = {"item": 50}
        result = get_total(costs, ["item"], 1.0)
        assert result == 100.0

    @pytest.mark.unit
    def test_high_precision_tax_rounds_correctly(self) -> None:
        """Tax rates with many decimals round the result to 2 d.p."""
        costs = {"item": 10}
        result = get_total(costs, ["item"], 0.12345)
        # 10 × 1.12345 = 11.2345 → 11.23
        assert result == 11.23

    @pytest.mark.unit
    def test_small_tax_rate(self) -> None:
        """Very small tax rate (0.1% = 0.001) is applied correctly."""
        costs = {"item": 100}
        result = get_total(costs, ["item"], 0.001)
        # 100 × 1.001 = 100.1
        assert result == 100.1


# ─── Edge Cases ───────────────────────────────────────────────────────────────

class TestEdgeCases:
    """Boundary conditions and unusual but valid inputs."""

    @pytest.mark.edge_case
    def test_empty_items_list_returns_zero(
        self, sample_costs: dict[str, float]
    ) -> None:
        """No items purchased → total is 0.0."""
        result = get_total(sample_costs, [], 0.09)
        assert result == 0.0

    @pytest.mark.edge_case
    def test_empty_catalogue_with_items_returns_zero(self) -> None:
        """Empty catalogue → all items skipped → total is 0.0."""
        result = get_total({}, ["socks", "shoes"], 0.09)
        assert result == 0.0

    @pytest.mark.edge_case
    def test_duplicate_items_counted_individually(self) -> None:
        """Buying the same item twice applies the price twice."""
        costs = {"socks": 5}
        result = get_total(costs, ["socks", "socks"], 0.0)
        assert result == 10.0

    @pytest.mark.edge_case
    def test_single_item_no_tax(self) -> None:
        """Single item with 0% tax returns the item price exactly."""
        costs = {"pen": 2.5}
        result = get_total(costs, ["pen"], 0.0)
        assert result == 2.5

    @pytest.mark.edge_case
    def test_large_catalogue_and_many_items(self) -> None:
        """Large inputs are handled within a reasonable time."""
        costs = {f"item_{i}": i * 1.5 for i in range(1000)}
        items = [f"item_{i}" for i in range(1000)]
        result = get_total(costs, items, 0.0)
        # Sum of 0*1.5 + 1*1.5 + ... + 999*1.5 = 1.5 * (999*1000/2)
        expected = round(1.5 * (999 * 1000 / 2), 2)
        assert result == expected

    @pytest.mark.edge_case
    def test_float_prices_in_catalogue(self) -> None:
        """Float prices in the catalogue compute accurately."""
        costs = {"coffee": 3.75, "muffin": 2.50}
        result = get_total(costs, ["coffee", "muffin"], 0.08)
        # 6.25 × 1.08 = 6.75
        assert result == 6.75

    @pytest.mark.edge_case
    def test_mixed_known_and_unknown_items(
        self, sample_costs: dict[str, float]
    ) -> None:
        """Mix of known and unknown items: only known ones are totalled."""
        result = get_total(sample_costs, ["socks", "jet", "hat", "rocket"], 0.0)
        # socks(5) + hat(15) = 20
        assert result == 20.0


# ─── Error Handling ───────────────────────────────────────────────────────────

class TestErrorHandling:
    """Validates defensive type checking on all parameters."""

    @pytest.mark.error_handling
    def test_raises_type_error_for_non_dict_costs(self) -> None:
        """Non-dict ``costs`` argument raises TypeError."""
        with pytest.raises(TypeError, match="'costs' must be a dict"):
            get_total([("socks", 5)], ["socks"], 0.09)  # type: ignore[arg-type]

    @pytest.mark.error_handling
    def test_raises_type_error_for_non_list_items(self) -> None:
        """Non-list ``items`` argument raises TypeError."""
        with pytest.raises(TypeError, match="'items' must be a list or tuple"):
            get_total({"socks": 5}, "socks", 0.09)  # type: ignore[arg-type]

    @pytest.mark.error_handling
    def test_raises_type_error_for_non_numeric_tax(self) -> None:
        """Non-numeric ``tax_rate`` raises TypeError."""
        with pytest.raises(TypeError, match="'tax_rate' must be numeric"):
            get_total({"socks": 5}, ["socks"], "0.09")  # type: ignore[arg-type]

    @pytest.mark.error_handling
    def test_raises_value_error_for_negative_tax(self) -> None:
        """Negative ``tax_rate`` raises ValueError."""
        with pytest.raises(ValueError, match="'tax_rate' must be >= 0"):
            get_total({"socks": 5}, ["socks"], -0.05)


# ─── format_receipt ───────────────────────────────────────────────────────────

class TestFormatReceipt:
    """Tests for the ``format_receipt`` helper function."""

    @pytest.mark.unit
    def test_receipt_contains_total(self) -> None:
        """The receipt output includes the correct total."""
        costs = {"socks": 5, "shoes": 60}
        receipt = format_receipt(costs, ["socks", "shoes"], 0.09)
        assert "70.85" in receipt

    @pytest.mark.unit
    def test_receipt_contains_all_purchased_items(self) -> None:
        """Each purchased item appears as a line in the receipt."""
        costs = {"coffee": 3.75, "muffin": 2.50}
        receipt = format_receipt(costs, ["coffee", "muffin"], 0.08)
        assert "coffee" in receipt
        assert "muffin" in receipt

    @pytest.mark.unit
    def test_receipt_uses_custom_currency_symbol(self) -> None:
        """Receipt respects a custom currency symbol."""
        costs = {"item": 10}
        receipt = format_receipt(costs, ["item"], 0.0, currency_symbol="€")
        assert "€" in receipt
        assert "$" not in receipt
