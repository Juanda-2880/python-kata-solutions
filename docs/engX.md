# Engineering Practices — EPAM engX Methodology

> This document defines the engineering standards and practices applied throughout the
> `python-kata-solutions` project, aligned with the **EPAM engX** (Engineering Excellence)
> methodology.

---

## 1. What Is EPAM engX?

**engX** (Engineering Excellence) is EPAM's proprietary framework for delivering
high-quality software through disciplined engineering practices. It covers the full
software development lifecycle (SDLC), from backlog grooming to production deployment,
and emphasises:

- **Predictability** — clearly defined processes reduce uncertainty.
- **Quality by design** — quality is built in, not tested in at the end.
- **Continuous improvement** — retrospectives and metrics drive iterative refinement.
- **Engineering ownership** — developers are responsible for design, implementation, testing, and delivery.

---

## 2. How engX Is Applied in This Project

### 2.1 Development Workflow

```
main (production-ready)
  └── develop (integration branch)
        ├── feature/US-001-dictionary-class
        ├── feature/US-002-shopping-calculator
        └── feature/US-003-nth-letter-extractor
```

**Branch naming convention:**

```
feature/US-XXX-short-description   # New functionality
bugfix/BUG-XXX-short-description   # Defect resolution
refactor/REFAC-XXX-description     # Non-functional improvements
hotfix/HF-XXX-critical-fix         # Production emergency patches
```

**Commit message convention (Conventional Commits):**

```
feat(dictionary): add remove() method with idempotent semantics
fix(shopping): correct rounding for high-precision tax rates
test(nth_letter): add unicode character edge case
docs(engineering): add engX methodology documentation
chore(deps): bump pytest to 8.2.0
```

### 2.2 Code Review Practices

All code must be reviewed before merging to `develop`. Reviews enforce:

| Checkpoint         | Standard                                                    |
| ------------------ | ----------------------------------------------------------- |
| PEP 8 compliance   | Enforced by `flake8` + `black` in CI                        |
| Type annotations   | All public functions and methods annotated                  |
| Docstring quality  | Google-style docstrings with Parameters, Returns, Raises    |
| Test coverage      | No merge if coverage drops below 90%                        |
| SOLID adherence    | Reviewer checks for SRP, OCP, DIP violations                |
| Security           | `bandit` scan must pass with no HIGH severity findings      |
| No debug artifacts | No `print()`, `breakpoint()`, or `TODO` left in merged code |

**Reviewer checklist (PR template):**

- [ ] Code is readable and self-documenting
- [ ] All business logic is covered by tests
- [ ] Edge cases are handled or explicitly excluded with reasoning
- [ ] No hardcoded secrets or magic numbers
- [ ] Logging is present for non-trivial operations
- [ ] Error messages are descriptive and actionable

### 2.3 CI/CD Pipeline

Defined in `.github/workflows/ci.yml`. Triggered on every push and pull request to
`develop` and `main`.

```
Push / PR
    │
    ├── 1. Lint (flake8 + black --check + isort --check)
    ├── 2. Type check (mypy --strict)
    ├── 3. Security scan (bandit)
    ├── 4. Unit tests (pytest -v)
    ├── 5. Coverage gate (≥ 90%)
    └── 6. Build package (python -m build)
```

No merge is permitted if any pipeline stage fails.

---

## 3. Code Quality Standards

### 3.1 PEP 8 & Formatting

- Line length: **99 characters** (configured in `pyproject.toml`).
- Formatter: `black` (non-negotiable, no manual formatting debates).
- Import order: `isort` with `black` profile.
- All files must end with a single newline.

### 3.2 Type System

- All public functions and methods carry **type annotations**.
- `mypy` runs in `--strict` mode; no `Any` allowed without explicit justification.
- Type aliases are used for complex types to improve readability
  (e.g. `CostCatalogue = dict[str, float | int]`).

### 3.3 Documentation Standards

Every module, class, and public method carries a docstring following
**Google-style** conventions:

```python
def my_function(param1: str, param2: int) -> bool:
    """Short imperative summary (under 79 chars).

    Extended description explaining behaviour, edge cases,
    and design rationale when non-obvious.

    Parameters
    ----------
    param1 : str
        Description of the first parameter.
    param2 : int
        Description of the second parameter.

    Returns
    -------
    bool
        What the return value represents.

    Raises
    ------
    ValueError
        When param2 is negative.

    Examples
    --------
    >>> my_function("hello", 1)
    True
    """
```

### 3.4 SOLID Principles Applied

| Principle                     | Application in This Project                                                                 |
| ----------------------------- | ------------------------------------------------------------------------------------------- |
| **S** — Single Responsibility | `Dictionary` only manages storage; I/O is caller's responsibility                           |
| **O** — Open/Closed           | `Dictionary` can be extended (e.g. `PersistentDictionary(Dictionary)`) without modification |
| **L** — Liskov Substitution   | Subclasses of `Dictionary` must honour its contract                                         |
| **I** — Interface Segregation | `nth_char` and `nth_char_safe` are separate functions, not a God class                      |
| **D** — Dependency Inversion  | Logging is injected via `logging.getLogger(__name__)`, not hardcoded                        |

### 3.5 Error Handling

- All public APIs validate input types explicitly with descriptive `TypeError` messages.
- Domain violations raise `ValueError` with actionable context.
- Functions never silently swallow unexpected exceptions.
- Logging (`DEBUG` level) tracks all non-trivial operations for observability.

---

## 4. Testing Strategy

### 4.1 Test Pyramid

```
           ┌─────────────────────┐
           │   Integration Tests  │   (few — cross-module flows)
           ├─────────────────────┤
           │     Unit Tests       │   (many — isolated logic)
           ├─────────────────────┤
           │  Edge Case / Error   │   (targeted — boundary validation)
           └─────────────────────┘
```

### 4.2 Test Organisation

Tests are grouped into **classes** by behaviour axis:

- `TestKataSpecification` — validates exact specification examples
- `TestEdgeCases` — boundary conditions, empty inputs, large inputs
- `TestErrorHandling` — type errors, value errors, invalid states
- `TestUtilityMethods` — supporting methods (size, contains, repr, etc.)

### 4.3 Coverage Expectations

| Module          | Target Coverage |
| --------------- | --------------- |
| `dictionary.py` | 100%            |
| `shopping.py`   | ≥ 95%           |
| `nth_letter.py` | 100%            |
| **Overall**     | **≥ 90%**       |

Coverage is measured via `pytest-cov` and enforced in CI via `--cov-fail-under=90`.

### 4.4 Test Naming Convention

```
test_<what>_<condition>_<expected_outcome>()

Examples:
    test_look_returns_definition_for_known_word()
    test_remove_absent_entry_returns_false()
    test_raises_type_error_for_non_string_word()
```

---

## 5. Security Considerations

- **No secrets in source code**: all environment-specific values use `.env` (gitignored).
- **`bandit` scans**: run on every CI pipeline execution; HIGH findings block merge.
- **Input validation**: all user-facing functions validate inputs before processing.
- **Dependency pinning**: `requirements.txt` and `requirements-dev.txt` use pinned versions
  to prevent supply-chain drift.
- **No eval/exec**: dynamic code execution is never used.

---

## 6. Maintainability Practices

- **Modular architecture**: each kata is an independent, self-contained module under `src/`.
- **Zero external runtime dependencies**: the runtime library uses only the Python standard
  library, eliminating transitive dependency risk.
- **Centralised configuration**: `pyproject.toml` is the single source of truth for all
  tool settings.
- **Logging configuration**: externalised to `config/logging.yaml`; no hardcoded log levels.
- **Changelog discipline**: all non-trivial changes documented in commit messages following
  Conventional Commits, enabling automatic changelog generation.
