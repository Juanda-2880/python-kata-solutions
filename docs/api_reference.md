# API Reference

> Complete reference for all public classes and functions in `kata_solutions`.
> All modules are located under `src/kata_solutions/`.

---

## Module: `kata_solutions.dictionary`

### Class: `Dictionary`

A class-based in-memory dictionary supporting entry creation and retrieval.

**Import:**

```python
from kata_solutions.dictionary import Dictionary
```

---

#### `Dictionary.__init__() → None`

Initialises an empty dictionary instance. No parameters required.

```python
d = Dictionary()
```

---

#### `Dictionary.newentry(word: str, definition: str) → None`

Adds a new word–definition pair, or overwrites an existing one.

| Parameter    | Type  | Description                                    |
| ------------ | ----- | ---------------------------------------------- |
| `word`       | `str` | Case-sensitive key to store.                   |
| `definition` | `str` | Textual definition to associate with the word. |

**Raises:** `TypeError` if either argument is not a `str`.

```python
d.newentry("Apple", "A fruit that grows on trees")
d.newentry("Apple", "Updated definition")  # overwrites silently
```

---

#### `Dictionary.look(word: str) → str`

Returns the definition for `word`, or a not-found message if absent.

| Parameter | Type  | Description                    |
| --------- | ----- | ------------------------------ |
| `word`    | `str` | Case-sensitive key to look up. |

**Returns:** `str` — the stored definition, or `"Can't find entry for {word}"`.  
**Raises:** `TypeError` if `word` is not a `str`.

```python
d.look("Apple")   # → "A fruit that grows on trees"
d.look("Banana")  # → "Can't find entry for Banana"
```

---

#### `Dictionary.remove(word: str) → bool`

Removes a word entry. Idempotent — returns `False` if the word was not present.

| Parameter | Type  | Description     |
| --------- | ----- | --------------- |
| `word`    | `str` | Word to remove. |

**Returns:** `True` if removed; `False` if not found.

---

#### `Dictionary.contains(word: str) → bool`

Checks existence without performing a full lookup.

**Returns:** `True` if `word` has an entry; `False` otherwise.

---

#### `Dictionary.size() → int`

Returns the total number of stored entries.

---

#### `Dictionary.entries() → dict[str, str]`

Returns a **shallow copy** of all entries. Mutating the result does not affect
the internal state.

---

#### Dunder Methods

| Method         | Behaviour                        |
| -------------- | -------------------------------- |
| `__len__`      | `len(d)` returns the entry count |
| `__contains__` | `"word" in d` membership test    |
| `__repr__`     | `Dictionary(entries=3)` format   |

---

## Module: `kata_solutions.shopping`

### Function: `get_total`

Calculates the total purchase cost of items, including a tax rate.

**Import:**

```python
from kata_solutions.shopping import get_total
```

#### Signature

```python
def get_total(
    costs: dict[str, float | int],
    items: Sequence[str],
    tax_rate: float,
) -> float:
```

#### Parameters

| Parameter  | Type                      | Description                                                            |
| ---------- | ------------------------- | ---------------------------------------------------------------------- |
| `costs`    | `dict[str, float \| int]` | Price catalogue mapping item name → unit price.                        |
| `items`    | `Sequence[str]`           | Ordered list of items to purchase. Duplicates are priced individually. |
| `tax_rate` | `float`                   | Fractional tax rate. `0.09` = 9%. Must be ≥ 0.                         |

#### Returns

`float` — Total cost rounded to 2 decimal places, including tax. Returns `0.0` if
no items match the catalogue.

#### Raises

| Exception    | Condition                                                                      |
| ------------ | ------------------------------------------------------------------------------ |
| `TypeError`  | `costs` is not `dict`, `items` is not a sequence, or `tax_rate` is not numeric |
| `ValueError` | `tax_rate` is negative                                                         |

#### Examples

```python
costs = {"socks": 5, "shoes": 60, "sweater": 30}

get_total(costs, ["socks", "shoes"], 0.09)   # → 70.85
get_total(costs, ["socks", "hat"], 0.10)     # → 5.5  ("hat" not in catalogue)
get_total(costs, [], 0.09)                   # → 0.0
get_total(costs, ["socks", "socks"], 0.00)   # → 10.0 (duplicate priced twice)
```

---

### Function: `format_receipt`

Generates a formatted multi-line receipt string for a purchase.

**Import:**

```python
from kata_solutions.shopping.shopping import format_receipt
```

#### Signature

```python
def format_receipt(
    costs: CostCatalogue,
    items: Sequence[str],
    tax_rate: float,
    currency_symbol: str = "$",
) -> str:
```

#### Parameters

| Parameter         | Type            | Default | Description                        |
| ----------------- | --------------- | ------- | ---------------------------------- |
| `costs`           | `CostCatalogue` | —       | Same as `get_total`.               |
| `items`           | `Sequence[str]` | —       | Same as `get_total`.               |
| `tax_rate`        | `float`         | —       | Same as `get_total`.               |
| `currency_symbol` | `str`           | `"$"`   | Prefix symbol for monetary values. |

#### Returns

`str` — A multi-line formatted receipt. Example output:

```
── Receipt ──────────────────
  socks          $   5.00
  shoes          $  60.00
────────────────────────────
  Subtotal       $  65.00
  Tax (9.00%)    $   5.85
  TOTAL          $  70.85
────────────────────────────
```

---

## Module: `kata_solutions.nth_letter`

### Function: `nth_char`

Extracts the character at position `n` from each word at index `n` and concatenates results.

**Import:**

```python
from kata_solutions.nth_letter import nth_char
```

#### Signature

```python
def nth_char(words: Sequence[str]) -> str:
```

#### Parameters

| Parameter | Type            | Description                                                                          |
| --------- | --------------- | ------------------------------------------------------------------------------------ |
| `words`   | `Sequence[str]` | Ordered list of words. Each word at index `n` must have at least `n + 1` characters. |

#### Returns

`str` — Concatenated nth characters. `""` for empty input.

#### Raises

| Exception    | Condition                                                       |
| ------------ | --------------------------------------------------------------- |
| `TypeError`  | `words` is not a `list` or `tuple`, or any element is not `str` |
| `IndexError` | A word at index `n` has fewer than `n + 1` characters           |

#### Examples

```python
nth_char(["yoda", "best", "has"])   # → "yes"
nth_char([])                         # → ""
nth_char(["abc", "xyz", "mno"])     # → "ayo"
nth_char(["YODA", "BEST", "HAS"])   # → "YES"
```

---

### Function: `nth_char_safe`

Lenient variant of `nth_char` that silently skips words too short for their index.

**Import:**

```python
from kata_solutions.nth_letter.nth_letter import nth_char_safe
```

#### Signature

```python
def nth_char_safe(words: Sequence[str]) -> str:
```

Identical contract to `nth_char` except:

- Does **not** raise `IndexError` for short words — they are silently omitted.
- Result may be shorter than `len(words)`.

```python
nth_char_safe(["ab", "c"])   # → "a"  ("c"[1] is OOB → skipped)
nth_char_safe([])             # → ""
```

---

## Type Aliases

| Alias            | Definition                | Module                                 |
| ---------------- | ------------------------- | -------------------------------------- |
| `CostCatalogue`  | `dict[str, float \| int]` | `kata_solutions.shopping.shopping`     |
| `DictionaryType` | `Optional[Dictionary]`    | `kata_solutions.dictionary.dictionary` |
