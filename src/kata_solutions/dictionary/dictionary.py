"""
kata_solutions.dictionary.dictionary
=====================================

Kata 1 — Custom Dictionary

Implements a class-based dictionary that supports adding word entries with
their definitions and looking up those definitions by key. Lookup returns a
descriptive not-found message rather than raising an exception, making it
safe to call without prior existence checks.

Design Decisions
----------------
- Internal storage uses a plain Python ``dict`` (O(1) average-case lookup).
- The class is intentionally single-responsibility: it stores and retrieves
  string entries. Persistence, serialisation, and bulk-import are out of scope
  for this kata but could be added via composition (e.g. a ``DictionaryLoader``
  collaborator) without modifying this class (Open/Closed Principle).
- All public methods are type-annotated and documented so IDEs and type-checkers
  can surface errors before runtime.

Usage
-----
>>> d = Dictionary()
>>> d.newentry("Apple", "A fruit that grows on trees")
>>> d.look("Apple")
'A fruit that grows on trees'
>>> d.look("Banana")
"Can't find entry for Banana"
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class Dictionary:
    """A simple in-memory word dictionary supporting entry creation and lookup.

    The ``Dictionary`` class maintains a mapping of words (keys) to their
    textual definitions (values). It provides a friendly not-found message
    when a requested word has no entry, rather than raising a ``KeyError``.

    Attributes
    ----------
    _entries : dict[str, str]
        Internal storage mapping words to their definitions.
        Not exposed publicly to enforce encapsulation; use ``newentry``
        and ``look`` to interact with the dictionary.

    Examples
    --------
    >>> d = Dictionary()
    >>> d.newentry("Python", "A high-level programming language")
    >>> d.look("Python")
    'A high-level programming language'
    >>> d.look("Cobol")
    "Can't find entry for Cobol"
    """

    def __init__(self) -> None:
        """Initialise an empty Dictionary instance."""
        self._entries: dict[str, str] = {}
        logger.debug("Dictionary instance created.")

    def newentry(self, word: str, definition: str) -> None:
        """Add or overwrite a word entry in the dictionary.

        If the word already exists, its definition is silently overwritten.
        This behaviour mirrors standard dictionary semantics where a later
        assignment supersedes an earlier one.

        Parameters
        ----------
        word : str
            The word or phrase to store. Case-sensitive: "apple" and "Apple"
            are treated as distinct keys.
        definition : str
            The textual definition to associate with ``word``.

        Raises
        ------
        TypeError
            If ``word`` or ``definition`` is not a string.

        Examples
        --------
        >>> d = Dictionary()
        >>> d.newentry("Cloud", "A visible mass of condensed water vapour")
        >>> d.look("Cloud")
        'A visible mass of condensed water vapour'

        >>> d.newentry("Cloud", "Overcast: used to indicate cloudy weather")
        >>> d.look("Cloud")
        'Overcast: used to indicate cloudy weather'
        """
        if not isinstance(word, str):
            raise TypeError(f"'word' must be a str, got {type(word).__name__!r}")
        if not isinstance(definition, str):
            raise TypeError(
                f"'definition' must be a str, got {type(definition).__name__!r}"
            )

        action = "Updated" if word in self._entries else "Added"
        self._entries[word] = definition
        logger.debug("%s entry: %r → %r", action, word, definition)

    def look(self, word: str) -> str:
        """Look up the definition of a word in the dictionary.

        Returns the stored definition when ``word`` is found, or a descriptive
        not-found message when it is absent — no exception is raised for missing
        keys.

        Parameters
        ----------
        word : str
            The word to look up. Case-sensitive.

        Returns
        -------
        str
            The stored definition if ``word`` exists, otherwise the string
            ``"Can't find entry for <word>"``.

        Raises
        ------
        TypeError
            If ``word`` is not a string.

        Examples
        --------
        >>> d = Dictionary()
        >>> d.newentry("Kernel", "The core component of an operating system")
        >>> d.look("Kernel")
        'The core component of an operating system'
        >>> d.look("Middleware")
        "Can't find entry for Middleware"
        """
        if not isinstance(word, str):
            raise TypeError(f"'word' must be a str, got {type(word).__name__!r}")

        if word in self._entries:
            definition = self._entries[word]
            logger.debug("Lookup hit: %r → %r", word, definition)
            return definition

        logger.debug("Lookup miss: %r", word)
        return f"Can't find entry for {word}"

    def remove(self, word: str) -> bool:
        """Remove a word entry from the dictionary.

        Parameters
        ----------
        word : str
            The word to remove.

        Returns
        -------
        bool
            ``True`` if the word was found and removed; ``False`` if it did
            not exist (idempotent — no exception raised).

        Raises
        ------
        TypeError
            If ``word`` is not a string.
        """
        if not isinstance(word, str):
            raise TypeError(f"'word' must be a str, got {type(word).__name__!r}")

        removed = self._entries.pop(word, None) is not None
        logger.debug("Remove %r: %s", word, "success" if removed else "not found")
        return removed

    def size(self) -> int:
        """Return the total number of entries currently stored.

        Returns
        -------
        int
            Count of stored word–definition pairs.
        """
        return len(self._entries)

    def contains(self, word: str) -> bool:
        """Check whether a word exists in the dictionary without a full lookup.

        Prefer this over ``look`` when the caller only needs to verify
        existence, not retrieve the definition.

        Parameters
        ----------
        word : str
            The word to check.

        Returns
        -------
        bool
            ``True`` if ``word`` has an entry; ``False`` otherwise.
        """
        if not isinstance(word, str):
            raise TypeError(f"'word' must be a str, got {type(word).__name__!r}")
        return word in self._entries

    def entries(self) -> dict[str, str]:
        """Return a shallow copy of all stored entries.

        A copy is returned (not the internal dict) to protect encapsulation:
        callers cannot mutate the internal state through the returned object.

        Returns
        -------
        dict[str, str]
            All word–definition pairs currently stored.
        """
        return dict(self._entries)

    def __repr__(self) -> str:
        """Unambiguous string representation for debugging."""
        return f"Dictionary(entries={self.size()})"

    def __len__(self) -> int:
        """Support ``len(dictionary_instance)``."""
        return self.size()

    def __contains__(self, word: object) -> bool:
        """Support ``'word' in dictionary_instance`` membership test."""
        return isinstance(word, str) and word in self._entries


# ─── Optional: convenience type alias for external consumers ──────────────────
DictionaryType = Optional[Dictionary]
