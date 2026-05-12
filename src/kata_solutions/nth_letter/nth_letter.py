"""
kata_solutions.nth_letter.nth_letter
======================================

Kata 3 — Nth Letter Extractor

Given a list of words, extract the character at position ``n`` from each word,
where ``n`` is the word's zero-based index in the list, then concatenate the
extracted characters into a single result string.

Algorithm
---------
For each word at index ``n``:
    result += word[n]

So for ``["yoda", "best", "has"]``:
    - Index 0: "yoda"[0] → "y"
    - Index 1: "best"[1] → "e"
    - Index 2: "has"[2]  → "s"
    → "yes"

Design Notes
------------
- The implementation uses ``enumerate`` for idiomatic index–value pairing.
- A ``join`` on a generator expression avoids intermediate list allocation.
- The kata specification guarantees each word has sufficient characters for
  its index (i.e. ``len(word) > n``), but this implementation validates
  defensively and raises ``IndexError`` with a descriptive message rather
  than letting Python emit a cryptic one.
- An empty list input is explicitly handled and returns an empty string.

Usage
-----
>>> nth_char(["yoda", "best", "has"])
'yes'
>>> nth_char([])
''
>>> nth_char(["abc"])
'a'
"""

import logging
from collections.abc import Sequence

logger = logging.getLogger(__name__)


def nth_char(words: Sequence[str]) -> str:
    """Construct a word by extracting the nth character from each word in a list.

    For every word in ``words``, the character at position ``n`` (where ``n``
    is the word's zero-based index in the list) is extracted. All such
    characters are concatenated in order to form the result string.

    Parameters
    ----------
    words : Sequence[str]
        An ordered collection of strings. Each string at index ``n`` must
        contain at least ``n + 1`` characters (i.e. ``len(word) > n``).
        An empty sequence returns an empty string without error.

    Returns
    -------
    str
        A string formed by concatenating the character at position ``n``
        from each word at index ``n``. Returns ``""`` for an empty input.

    Raises
    ------
    TypeError
        If ``words`` is not a sequence, or if any element is not a ``str``.
    IndexError
        If any word at index ``n`` has fewer than ``n + 1`` characters,
        meaning the required character position is out of bounds.

    Examples
    --------
    >>> nth_char(["yoda", "best", "has"])
    'yes'

    >>> nth_char([])
    ''

    >>> nth_char(["a"])
    'a'

    >>> nth_char(["abc", "xyz", "mno"])
    'ay'  # 'a' from index 0, 'y' from index 1, 'o' from index 2 → 'ayo'

    Notes
    -----
    The function is case-preserving: uppercase characters in the source words
    appear as uppercase in the result.

    >>> nth_char(["YODA", "BEST", "HAS"])
    'YES'
    """
    # ── Input validation ─────────────────────────────────────────────────────
    if not isinstance(words, (list, tuple)):
        raise TypeError(
            f"'words' must be a list or tuple, got {type(words).__name__!r}"
        )

    if not words:
        logger.debug("nth_char called with empty list — returning empty string.")
        return ""

    # ── Core extraction ───────────────────────────────────────────────────────
    result_chars: list[str] = []

    for index, word in enumerate(words):
        if not isinstance(word, str):
            raise TypeError(
                f"All elements of 'words' must be str. "
                f"Element at index {index} is {type(word).__name__!r}: {word!r}"
            )

        if len(word) <= index:
            raise IndexError(
                f"Word at index {index} ({word!r}) has {len(word)} character(s), "
                f"but character at position {index} is required. "
                f"Ensure each word has at least (index + 1) characters."
            )

        char = word[index]
        result_chars.append(char)
        logger.debug(
            "Index %d | word=%r | char=%r (position %d)", index, word, char, index
        )

    result = "".join(result_chars)
    logger.debug("nth_char result: %r from words=%r", result, list(words))
    return result


def nth_char_safe(words: Sequence[str]) -> str:
    """Variant of ``nth_char`` that silently skips out-of-bounds words.

    Unlike the strict ``nth_char``, this function does not raise an
    ``IndexError`` when a word is too short for its index. Instead, it
    simply omits that word's contribution from the result. This may be
    useful in lenient parsing contexts.

    Parameters
    ----------
    words : Sequence[str]
        An ordered collection of strings. Words that are too short for
        their index position are silently skipped.

    Returns
    -------
    str
        A string formed by concatenating valid nth characters. May be
        shorter than ``len(words)`` if some words were too short.

    Examples
    --------
    >>> nth_char_safe(["yoda", "hi", "has"])
    'ys'  # "hi"[1] is 'i', but "hi" has index 1 so this works. "hi" with index 2 skipped.
    >>> nth_char_safe(["ab", "c"])
    'a'  # "c"[1] is out of bounds → skipped
    """
    if not isinstance(words, (list, tuple)):
        raise TypeError(
            f"'words' must be a list or tuple, got {type(words).__name__!r}"
        )

    result_chars: list[str] = []

    for index, word in enumerate(words):
        if not isinstance(word, str):
            logger.warning("Skipping non-str element at index %d: %r", index, word)
            continue
        if len(word) > index:
            result_chars.append(word[index])
        else:
            logger.warning(
                "Word %r at index %d is too short (len=%d) — skipped.",
                word, index, len(word)
            )

    return "".join(result_chars)
