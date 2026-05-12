"""
tests/test_dictionary.py
=========================

Unit tests for ``kata_solutions.dictionary.Dictionary``.

Test Strategy
-------------
Tests are grouped into logical classes that mirror the Dictionary's public API.
Each class isolates a single behaviour axis, making failures easy to diagnose.

Coverage Targets
----------------
- Happy path: add and retrieve entries               ✓
- Not-found message format                           ✓
- Entry overwrite (idempotent newentry)              ✓
- Type validation (TypeError on non-str inputs)     ✓
- remove(), contains(), size(), entries(), len()     ✓
- __contains__ dunder (``in`` operator)              ✓
- __repr__ string                                    ✓
- Edge cases: empty string key/value, long strings   ✓
"""

import pytest

from kata_solutions.dictionary import Dictionary


# ─── Kata Core Behaviour ──────────────────────────────────────────────────────

class TestKataSpecification:
    """Validates the exact behaviour described in the kata specification."""

    def test_look_returns_definition_for_known_word(
        self, populated_dictionary: Dictionary
    ) -> None:
        """``look`` returns the stored definition when word exists."""
        assert populated_dictionary.look("Apple") == "A fruit that grows on trees"

    def test_look_returns_not_found_message_for_unknown_word(
        self, populated_dictionary: Dictionary
    ) -> None:
        """``look`` returns a descriptive message for words not in the dictionary."""
        result = populated_dictionary.look("Banana")
        assert result == "Can't find entry for Banana"

    def test_not_found_message_includes_word(self, empty_dictionary: Dictionary) -> None:
        """The not-found message dynamically embeds the looked-up word."""
        word = "Extraordinary"
        result = empty_dictionary.look(word)
        assert word in result

    def test_kata_full_workflow(self) -> None:
        """Replicates the complete kata example from the specification verbatim."""
        d = Dictionary()
        d.newentry("Apple", "A fruit that grows on trees")

        assert d.look("Apple") == "A fruit that grows on trees"
        assert d.look("Banana") == "Can't find entry for Banana"


# ─── newentry ─────────────────────────────────────────────────────────────────

class TestNewentry:
    """Tests for the ``newentry`` method."""

    @pytest.mark.unit
    def test_newentry_adds_single_entry(self, empty_dictionary: Dictionary) -> None:
        """Adding one entry increments size to 1."""
        empty_dictionary.newentry("Key", "Value")
        assert empty_dictionary.size() == 1

    @pytest.mark.unit
    def test_newentry_multiple_entries(self, empty_dictionary: Dictionary) -> None:
        """Multiple entries are all stored and individually retrievable."""
        entries = {"Alpha": "First", "Beta": "Second", "Gamma": "Third"}
        for word, defn in entries.items():
            empty_dictionary.newentry(word, defn)

        for word, expected_defn in entries.items():
            assert empty_dictionary.look(word) == expected_defn

    @pytest.mark.unit
    def test_newentry_overwrites_existing_definition(
        self, empty_dictionary: Dictionary
    ) -> None:
        """Adding the same word twice updates, not duplicates, the entry."""
        empty_dictionary.newentry("Cloud", "Original definition")
        empty_dictionary.newentry("Cloud", "Updated definition")

        assert empty_dictionary.look("Cloud") == "Updated definition"
        assert empty_dictionary.size() == 1

    @pytest.mark.unit
    def test_newentry_empty_string_key(self, empty_dictionary: Dictionary) -> None:
        """An empty string is a valid (if unusual) key."""
        empty_dictionary.newentry("", "Definition for empty key")
        assert empty_dictionary.look("") == "Definition for empty key"

    @pytest.mark.unit
    def test_newentry_empty_string_definition(self, empty_dictionary: Dictionary) -> None:
        """An empty string definition is stored as-is."""
        empty_dictionary.newentry("EmptyDef", "")
        assert empty_dictionary.look("EmptyDef") == ""

    @pytest.mark.error_handling
    def test_newentry_raises_type_error_for_non_string_word(
        self, empty_dictionary: Dictionary
    ) -> None:
        """Non-string word raises TypeError."""
        with pytest.raises(TypeError, match="'word' must be a str"):
            empty_dictionary.newentry(123, "some definition")  # type: ignore[arg-type]

    @pytest.mark.error_handling
    def test_newentry_raises_type_error_for_non_string_definition(
        self, empty_dictionary: Dictionary
    ) -> None:
        """Non-string definition raises TypeError."""
        with pytest.raises(TypeError, match="'definition' must be a str"):
            empty_dictionary.newentry("word", ["list", "is", "not", "string"])  # type: ignore[arg-type]


# ─── look ─────────────────────────────────────────────────────────────────────

class TestLook:
    """Tests for the ``look`` method."""

    @pytest.mark.unit
    def test_look_case_sensitive(self, empty_dictionary: Dictionary) -> None:
        """Lookup is case-sensitive: 'apple' ≠ 'Apple'."""
        empty_dictionary.newentry("apple", "lowercase definition")
        assert empty_dictionary.look("Apple") == "Can't find entry for Apple"
        assert empty_dictionary.look("apple") == "lowercase definition"

    @pytest.mark.unit
    def test_look_whitespace_key(self, empty_dictionary: Dictionary) -> None:
        """Keys with leading/trailing whitespace are treated literally."""
        empty_dictionary.newentry(" padded ", "padded key")
        assert empty_dictionary.look(" padded ") == "padded key"
        assert empty_dictionary.look("padded") == "Can't find entry for padded"

    @pytest.mark.error_handling
    def test_look_raises_type_error_for_non_string(
        self, empty_dictionary: Dictionary
    ) -> None:
        """Non-string lookup word raises TypeError."""
        with pytest.raises(TypeError, match="'word' must be a str"):
            empty_dictionary.look(None)  # type: ignore[arg-type]

    @pytest.mark.edge_case
    def test_look_long_word(self, empty_dictionary: Dictionary) -> None:
        """Very long words are stored and retrieved correctly."""
        long_word = "a" * 10_000
        empty_dictionary.newentry(long_word, "long key definition")
        assert empty_dictionary.look(long_word) == "long key definition"


# ─── remove ───────────────────────────────────────────────────────────────────

class TestRemove:
    """Tests for the ``remove`` method."""

    @pytest.mark.unit
    def test_remove_existing_entry_returns_true(
        self, populated_dictionary: Dictionary
    ) -> None:
        """Removing a present word returns True and decrements size."""
        size_before = populated_dictionary.size()
        result = populated_dictionary.remove("Apple")
        assert result is True
        assert populated_dictionary.size() == size_before - 1

    @pytest.mark.unit
    def test_remove_existing_entry_makes_it_unreachable(
        self, empty_dictionary: Dictionary
    ) -> None:
        """After removal, ``look`` returns the not-found message."""
        empty_dictionary.newentry("Temp", "Temporary entry")
        empty_dictionary.remove("Temp")
        assert empty_dictionary.look("Temp") == "Can't find entry for Temp"

    @pytest.mark.unit
    def test_remove_absent_entry_returns_false(
        self, empty_dictionary: Dictionary
    ) -> None:
        """Removing a word that was never added returns False (idempotent)."""
        result = empty_dictionary.remove("NeverAdded")
        assert result is False

    @pytest.mark.edge_case
    def test_remove_same_key_twice_is_safe(self, empty_dictionary: Dictionary) -> None:
        """Removing the same key twice does not raise; second call returns False."""
        empty_dictionary.newentry("Once", "Only once")
        assert empty_dictionary.remove("Once") is True
        assert empty_dictionary.remove("Once") is False


# ─── Utility Methods ──────────────────────────────────────────────────────────

class TestUtilityMethods:
    """Tests for size, contains, entries, len, and dunder methods."""

    @pytest.mark.unit
    def test_size_empty_dictionary(self, empty_dictionary: Dictionary) -> None:
        """Empty dictionary reports size 0."""
        assert empty_dictionary.size() == 0

    @pytest.mark.unit
    def test_len_equals_size(self, populated_dictionary: Dictionary) -> None:
        """``len()`` and ``.size()`` return the same value."""
        assert len(populated_dictionary) == populated_dictionary.size()

    @pytest.mark.unit
    def test_contains_method_true_for_existing(
        self, populated_dictionary: Dictionary
    ) -> None:
        """``contains`` returns True for a word that exists."""
        assert populated_dictionary.contains("Python") is True

    @pytest.mark.unit
    def test_contains_method_false_for_missing(
        self, populated_dictionary: Dictionary
    ) -> None:
        """``contains`` returns False for a word that does not exist."""
        assert populated_dictionary.contains("Rust") is False

    @pytest.mark.unit
    def test_in_operator(self, populated_dictionary: Dictionary) -> None:
        """The ``in`` membership operator works via __contains__."""
        assert "Apple" in populated_dictionary
        assert "Banana" not in populated_dictionary

    @pytest.mark.unit
    def test_entries_returns_copy(self, populated_dictionary: Dictionary) -> None:
        """``entries()`` returns a copy; mutating it does not affect the dictionary."""
        snapshot = populated_dictionary.entries()
        snapshot["Injected"] = "Should not appear"
        assert "Injected" not in populated_dictionary

    @pytest.mark.unit
    def test_repr_includes_entry_count(self, populated_dictionary: Dictionary) -> None:
        """``repr()`` contains the entry count for debugging."""
        r = repr(populated_dictionary)
        assert "Dictionary" in r
        assert str(populated_dictionary.size()) in r
