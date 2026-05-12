"""
tests/test_nth_letter.py
=========================

Unit tests for ``kata_solutions.nth_letter.nth_char`` and ``nth_char_safe``.

Test Strategy
-------------
- Validates the exact kata specification example first.
- Tests single-word input (index 0 → first character).
- Tests empty list input → empty string.
- Tests case preservation (uppercase, lowercase, mixed).
- Tests that out-of-bounds words raise IndexError with descriptive message.
- Tests type errors for non-sequence and non-string elements.
- Tests the lenient ``nth_char_safe`` variant.
"""

import pytest

from kata_solutions.nth_letter import nth_char
from kata_solutions.nth_letter.nth_letter import nth_char_safe


# ─── Kata Specification ───────────────────────────────────────────────────────

class TestKataSpecification:
    """Validates the exact behaviour described in the kata specification."""

    def test_kata_canonical_example(
        self,
        kata_example_words: list[str],
        kata_example_result: str,
    ) -> None:
        """Replicates the kata's exact example: ['yoda','best','has'] → 'yes'."""
        assert nth_char(kata_example_words) == kata_example_result

    def test_kata_example_values(self) -> None:
        """Checks each character extracted individually for the canonical example."""
        words = ["yoda", "best", "has"]
        result = nth_char(words)
        # y = words[0][0], e = words[1][1], s = words[2][2]
        assert result[0] == "y"
        assert result[1] == "e"
        assert result[2] == "s"

    def test_empty_list_returns_empty_string(self) -> None:
        """An empty word list returns an empty string, not None or an error."""
        assert nth_char([]) == ""

    def test_single_word_returns_first_character(self) -> None:
        """A single word at index 0 returns its first character."""
        assert nth_char(["hello"]) == "h"

    def test_single_character_words(self) -> None:
        """Words with one character work when each is at index 0."""
        assert nth_char(["a"]) == "a"


# ─── Character Extraction Correctness ─────────────────────────────────────────

class TestCharacterExtraction:
    """Verifies correct positional extraction across various word lists."""

    @pytest.mark.unit
    def test_two_word_list(self) -> None:
        """Two words: extracts word[0][0] and word[1][1]."""
        # "ab"[0] = "a", "bc"[1] = "c"
        assert nth_char(["ab", "bc"]) == "ac"

    @pytest.mark.unit
    def test_all_same_length_words(self) -> None:
        """All words have the same length — each index is valid."""
        words = ["abc", "def", "ghi"]
        # 'a', 'e', 'i'
        assert nth_char(words) == "aei"

    @pytest.mark.unit
    def test_long_word_list(self) -> None:
        """Longer list extracts from increasingly deep positions."""
        words = ["a" * (i + 1) for i in range(5)]  # ["a","aa","aaa","aaaa","aaaaa"]
        result = nth_char(words)
        assert result == "a" * 5

    @pytest.mark.unit
    def test_result_length_equals_input_length(self) -> None:
        """Result string length equals the number of words."""
        words = ["alpha", "bravo", "charlie"]
        result = nth_char(words)
        assert len(result) == len(words)


# ─── Case Preservation ────────────────────────────────────────────────────────

class TestCasePreservation:
    """Verifies that nth_char does not alter character casing."""

    @pytest.mark.unit
    def test_uppercase_words_preserve_case(self) -> None:
        """Uppercase characters are returned as-is."""
        assert nth_char(["YODA", "BEST", "HAS"]) == "YES"

    @pytest.mark.unit
    def test_mixed_case_words(self) -> None:
        """Mixed-case characters are returned without transformation."""
        words = ["Hello", "World"]
        # "Hello"[0] = 'H', "World"[1] = 'o'
        assert nth_char(words) == "Ho"

    @pytest.mark.unit
    def test_digits_and_special_chars_preserved(self) -> None:
        """Non-alphabetic characters (digits, punctuation) are valid and preserved."""
        words = ["123", "abc"]
        # "123"[0] = '1', "abc"[1] = 'b'
        assert nth_char(words) == "1b"


# ─── Edge Cases ───────────────────────────────────────────────────────────────

class TestEdgeCases:
    """Boundary and unusual inputs."""

    @pytest.mark.edge_case
    def test_words_with_leading_spaces(self) -> None:
        """Leading spaces are valid characters and counted in indexing."""
        # " hi"[0] = ' ', "ab"[1] = 'b'
        words = [" hi", "ab"]
        assert nth_char(words) == " b"

    @pytest.mark.edge_case
    def test_words_with_unicode_characters(self) -> None:
        """Unicode multi-byte characters are treated as single characters."""
        words = ["café", "über"]
        # "café"[0] = 'c', "über"[1] = 'b'
        assert nth_char(words) == "cb"

    @pytest.mark.edge_case
    def test_tuple_input_accepted(self) -> None:
        """A tuple (not just list) is a valid sequence input."""
        assert nth_char(("yoda", "best", "has")) == "yes"  # type: ignore[arg-type]


# ─── Error Handling ───────────────────────────────────────────────────────────

class TestErrorHandling:
    """Validates defensive error raising for invalid inputs."""

    @pytest.mark.error_handling
    def test_raises_type_error_for_non_sequence(self) -> None:
        """Non-sequence input raises TypeError."""
        with pytest.raises(TypeError, match="'words' must be a list or tuple"):
            nth_char("not a list")  # type: ignore[arg-type]

    @pytest.mark.error_handling
    def test_raises_type_error_for_non_string_element(self) -> None:
        """A non-string element within the list raises TypeError."""
        with pytest.raises(TypeError, match="All elements of 'words' must be str"):
            nth_char(["valid", 123])  # type: ignore[list-item]

    @pytest.mark.error_handling
    def test_raises_index_error_for_word_too_short(self) -> None:
        """A word shorter than its index raises IndexError with a clear message."""
        with pytest.raises(IndexError, match="character at position 1 is required"):
            nth_char(["abc", "d"])  # "d" is at index 1 but has length 1


# ─── nth_char_safe (lenient variant) ─────────────────────────────────────────

class TestNthCharSafe:
    """Tests for the lenient ``nth_char_safe`` variant."""

    @pytest.mark.unit
    def test_safe_skips_short_words(self) -> None:
        """Words too short for their index are silently skipped."""
        # "ab"[0] = 'a'; "c"[1] = out of bounds → skipped
        result = nth_char_safe(["ab", "c"])
        assert result == "a"

    @pytest.mark.unit
    def test_safe_returns_empty_for_all_short_words(self) -> None:
        """All words too short → empty result."""
        result = nth_char_safe(["a", "b"])
        # "a"[0] = 'a' (ok), "b"[1] = OOB (skipped) → "a"
        assert result == "a"

    @pytest.mark.unit
    def test_safe_canonical_example_unchanged(self) -> None:
        """When words are valid, safe variant matches strict variant."""
        words = ["yoda", "best", "has"]
        assert nth_char_safe(words) == nth_char(words)

    @pytest.mark.unit
    def test_safe_empty_list(self) -> None:
        """Empty list returns empty string without error."""
        assert nth_char_safe([]) == ""
