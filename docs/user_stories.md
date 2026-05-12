# User Stories, Acceptance Criteria & Technical Tasks

> Agile artefacts for `python-kata-solutions` following EPAM engX backlog standards.
> Format: US = User Story | AC = Acceptance Criteria | TT = Technical Task | DoD = Definition of Done

---

## Epic: EP-001 — Python Kata Solution Suite

**Epic Goal:** Deliver three production-grade Python kata solutions structured as an
enterprise software project, following EPAM engX engineering standards, with complete
documentation, tests, and CI/CD.

**Business Value:** Demonstrate senior-level engineering capability across OOP design,
functional programming, algorithm design, testing strategy, and professional project
organisation.

---

## US-001 — Custom Dictionary Class

```
AS A   developer consuming the kata solution library,
I WANT a Dictionary class that stores word definitions and retrieves them by key,
SO THAT I can build dictionary-backed features without implementing storage logic myself.
```

**Story Points:** 3  
**Priority:** High  
**Sprint:** 1

### Acceptance Criteria

```gherkin
Feature: Custom Dictionary

  Scenario: Look up an existing word
    Given a Dictionary instance with "Apple" → "A fruit that grows on trees"
    When I call d.look("Apple")
    Then the result is "A fruit that grows on trees"

  Scenario: Look up a word that does not exist
    Given a Dictionary instance with no entry for "Banana"
    When I call d.look("Banana")
    Then the result is "Can't find entry for Banana"

  Scenario: Overwrite an existing entry
    Given a Dictionary with "Cloud" → "Old definition"
    When I call d.newentry("Cloud", "New definition")
    And I call d.look("Cloud")
    Then the result is "New definition"
    And the dictionary contains exactly 1 entry

  Scenario: Type validation
    Given a Dictionary instance
    When I call d.newentry(123, "value") with a non-string word
    Then a TypeError is raised with message containing "'word' must be a str"

  Scenario: Empty dictionary
    Given a freshly constructed Dictionary
    When I call d.size()
    Then the result is 0
```

### Technical Tasks

| ID       | Task                                                                         | Assignee | Status |
| -------- | ---------------------------------------------------------------------------- | -------- | ------ |
| TT-001-1 | Create `src/kata_solutions/dictionary/dictionary.py` with `Dictionary` class | Dev      | Done   |
| TT-001-2 | Implement `newentry(word, definition)` with type validation                  | Dev      | Done   |
| TT-001-3 | Implement `look(word)` returning definition or not-found message             | Dev      | Done   |
| TT-001-4 | Implement utility methods: `remove`, `contains`, `size`, `entries`           | Dev      | Done   |
| TT-001-5 | Add `__repr__`, `__len__`, `__contains__` dunder methods                     | Dev      | Done   |
| TT-001-6 | Write unit tests in `tests/test_dictionary.py` (≥ 90% coverage)              | Dev      | Done   |
| TT-001-7 | Add Google-style docstrings to all public methods                            | Dev      | Done   |
| TT-001-8 | Verify `mypy --strict` passes on the module                                  | Dev      | Done   |

---

## US-002 — Shopping Tax Calculator

```
AS A   purchasing system consumer,
I WANT a function that calculates total purchase cost given a price catalogue,
       item list, and tax rate,
SO THAT I can compute accurate totals including tax without manual calculation.
```

**Story Points:** 2  
**Priority:** High  
**Sprint:** 1

### Acceptance Criteria

```gherkin
Feature: Shopping Tax Calculator

  Scenario: Calculate total with known items and tax
    Given a cost catalogue {"socks": 5, "shoes": 60, "sweater": 30}
    And a purchase list ["socks", "shoes"]
    And a tax rate of 0.09 (9%)
    When I call get_total(costs, items, 0.09)
    Then the result is 70.85

  Scenario: Unknown items are silently ignored
    Given a cost catalogue {"socks": 5}
    And a purchase list ["socks", "unicorn"]
    When I call get_total(costs, items, 0.0)
    Then the result is 5.0
    And no error is raised

  Scenario: Result is rounded to two decimal places
    Given any price and tax combination
    When I call get_total
    Then the result has exactly two decimal places

  Scenario: Empty item list
    Given any cost catalogue
    And an empty purchase list []
    When I call get_total(costs, [], 0.09)
    Then the result is 0.0

  Scenario: Negative tax rate
    Given a valid cost catalogue and item list
    When I call get_total(costs, items, -0.05)
    Then a ValueError is raised with message containing "'tax_rate' must be >= 0"
```

### Technical Tasks

| ID       | Task                                                          | Assignee | Status |
| -------- | ------------------------------------------------------------- | -------- | ------ |
| TT-002-1 | Create `src/kata_solutions/shopping/shopping.py`              | Dev      | Done   |
| TT-002-2 | Implement `get_total(costs, items, tax_rate)` with rounding   | Dev      | Done   |
| TT-002-3 | Implement input validation (TypeError, ValueError)            | Dev      | Done   |
| TT-002-4 | Implement `format_receipt` helper function                    | Dev      | Done   |
| TT-002-5 | Write unit tests in `tests/test_shopping.py` (≥ 90% coverage) | Dev      | Done   |
| TT-002-6 | Document floating-point precision note in module docstring    | Dev      | Done   |

---

## US-003 — Nth Letter Word Extractor

```
AS A   string manipulation library consumer,
I WANT a function that extracts the nth character from each word in a list
       and concatenates the results,
SO THAT I can generate derived tokens from structured word sequences.
```

**Story Points:** 2  
**Priority:** High  
**Sprint:** 1

### Acceptance Criteria

```gherkin
Feature: Nth Letter Extractor

  Scenario: Extract characters per kata example
    Given the word list ["yoda", "best", "has"]
    When I call nth_char(words)
    Then the result is "yes"
    Because "yoda"[0]="y", "best"[1]="e", "has"[2]="s"

  Scenario: Empty list returns empty string
    Given an empty word list []
    When I call nth_char([])
    Then the result is "" (empty string)

  Scenario: Single word
    Given the word list ["hello"]
    When I call nth_char(["hello"])
    Then the result is "h" (word[0][0])

  Scenario: Word too short raises IndexError
    Given the word list ["abc", "d"]  — "d" has length 1 but is at index 1
    When I call nth_char(words)
    Then an IndexError is raised with "too short" in the message

  Scenario: Non-sequence input raises TypeError
    When I call nth_char("not a list")
    Then a TypeError is raised with "'words' must be a list or tuple"
```

### Technical Tasks

| ID       | Task                                                            | Assignee | Status |
| -------- | --------------------------------------------------------------- | -------- | ------ |
| TT-003-1 | Create `src/kata_solutions/nth_letter/nth_letter.py`            | Dev      | Done   |
| TT-003-2 | Implement `nth_char(words)` using enumerate + join              | Dev      | Done   |
| TT-003-3 | Implement `nth_char_safe(words)` lenient variant                | Dev      | Done   |
| TT-003-4 | Add defensive IndexError with descriptive message               | Dev      | Done   |
| TT-003-5 | Write unit tests in `tests/test_nth_letter.py` (≥ 90% coverage) | Dev      | Done   |
| TT-003-6 | Add unicode edge case test                                      | Dev      | Done   |

---

## US-004 — Project Infrastructure

```
AS A   team member onboarding to the project,
I WANT a complete repository structure with CI, documentation, and setup instructions,
SO THAT I can be productive from day one without manual environment archaeology.
```

**Story Points:** 5  
**Priority:** High  
**Sprint:** 1

### Acceptance Criteria

```gherkin
  Scenario: Developer can set up and run the project from scratch
    Given a fresh clone of the repository
    When I follow the README Quick Start instructions
    Then I can run all tests successfully
    And I can execute the demonstration script

  Scenario: CI pipeline runs on every push
    Given a push to any branch
    When GitHub Actions triggers the CI workflow
    Then lint, type check, security scan, tests, and coverage all run
    And a failing check blocks the merge

  Scenario: Documentation is complete
    Given the docs/ folder
    When I read engineering_practices.md, user_stories.md, and definition_of_done.md
    Then all EPAM engX artefacts are present and professional
```

### Technical Tasks

| ID       | Task                                                            | Assignee | Status |
| -------- | --------------------------------------------------------------- | -------- | ------ |
| TT-004-1 | Create repository with professional folder structure            | Dev      | Done   |
| TT-004-2 | Write `README.md` with setup, usage, and structure docs         | Dev      | Done   |
| TT-004-3 | Create `.gitignore`, `requirements.txt`, `requirements-dev.txt` | Dev      | Done   |
| TT-004-4 | Configure `pyproject.toml` with all tool settings               | Dev      | Done   |
| TT-004-5 | Create `.github/workflows/ci.yml` GitHub Actions pipeline       | Dev      | Done   |
| TT-004-6 | Create `docs/` with all engX documentation files                | Dev      | Done   |
| TT-004-7 | Create `scripts/run_all.py` demonstration runner                | Dev      | Done   |
| TT-004-8 | Create `config/logging.yaml` centralised logging config         | Dev      | Done   |
