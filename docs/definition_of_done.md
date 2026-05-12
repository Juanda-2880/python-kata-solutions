# Definition of Done (DoD)

> The **Definition of Done** is the shared team agreement on what "complete" means for any
> deliverable in `python-kata-solutions`. No User Story, Technical Task, or feature branch
> may be merged to `develop` unless **every item** in the applicable checklist is satisfied.
>
> This DoD is reviewed and updated at the end of each sprint during the Sprint Retrospective.

---

## DoD — User Story (Feature)

A User Story is **Done** when all of the following are true:

### Code Quality

- [ ] All code follows PEP 8; `flake8` reports zero violations
- [ ] `black --check` passes with no formatting differences
- [ ] `isort --check` passes with correct import ordering
- [ ] Line length ≤ 99 characters throughout
- [ ] No `TODO`, `FIXME`, `HACK`, `print()`, or `breakpoint()` left in production code
- [ ] No magic numbers — all constants are named and documented

### Type Safety

- [ ] All public functions and methods carry complete type annotations
- [ ] `mypy --strict` passes with zero errors on the module
- [ ] No use of `Any` without explicit `# type: ignore` comment and justification

### Documentation

- [ ] Every module has a top-level module docstring explaining purpose, design decisions, and usage
- [ ] Every public class has a class-level docstring with `Attributes` section
- [ ] Every public method/function has a Google-style docstring with:
  - `Parameters` block
  - `Returns` block
  - `Raises` block (if any exception is raised)
  - At least one `Examples` block
- [ ] `README.md` updated if any public API changed
- [ ] `docs/api_reference.md` updated if any public API changed

### Testing

- [ ] All business logic paths have at least one unit test
- [ ] All edge cases identified during implementation are covered by tests
- [ ] All error/exception paths have at least one test
- [ ] Test names follow the `test_<what>_<condition>_<expected>` convention
- [ ] No test relies on execution order (tests are fully independent)
- [ ] `pytest` passes with **zero failures**
- [ ] Module-level code coverage is **≥ 90%** (enforced by `--cov-fail-under=90`)
- [ ] No tests marked `@pytest.mark.skip` without an open ticket reference

### Security

- [ ] `bandit` scan reports zero HIGH severity issues
- [ ] No secrets, API keys, or credentials in source code
- [ ] All user-facing input is validated before processing

### CI/CD

- [ ] All CI pipeline stages pass on the feature branch:
  - Lint (flake8 + black + isort)
  - Type check (mypy)
  - Security scan (bandit)
  - Unit tests (pytest)
  - Coverage gate (≥ 90%)
- [ ] No pipeline warnings that were not present before this branch

### Review

- [ ] Pull Request created against `develop` with filled PR description
- [ ] At least **1 peer approval** received (2 for changes to public API)
- [ ] All review comments addressed or explicitly deferred with a ticket reference
- [ ] No unresolved conversation threads in the PR

### Acceptance

- [ ] All Acceptance Criteria from the User Story are demonstrably met
- [ ] Product Owner or Story Author has verified the behaviour
- [ ] Feature works correctly end-to-end in the `scripts/run_all.py` demonstration

---

## DoD — Technical Task (Sub-task)

A Technical Task is **Done** when:

- [ ] The implementation exactly matches the task description
- [ ] The code passes all relevant existing tests (no regressions)
- [ ] New tests are added if the task introduces new behaviour
- [ ] The PR is linked to the parent User Story
- [ ] At least 1 reviewer approval received

---

## DoD — Bug Fix

A Bug Fix is **Done** when:

- [ ] Root cause is identified and documented in the PR description
- [ ] A **regression test** is added that fails before the fix and passes after
- [ ] Fix does not introduce new `mypy`, `flake8`, or `bandit` violations
- [ ] All existing tests continue to pass
- [ ] The fix is verified in the original failure scenario

---

## DoD — Sprint

A Sprint is **Done** when:

- [ ] All committed User Stories meet their individual DoD
- [ ] `develop` branch is in a deployable state (all CI checks pass)
- [ ] Sprint Review has been conducted with stakeholders
- [ ] Sprint Retrospective actions are captured in the team backlog
- [ ] Technical debt items identified during the sprint are logged as backlog items
- [ ] Documentation is up to date with all sprint deliverables

---

## DoD — Release

A Release is **Done** when:

- [ ] All stories in the release scope meet their DoD
- [ ] `develop` is merged to `main` via a Release PR
- [ ] Version number bumped in `pyproject.toml` following SemVer
- [ ] Git tag created: `v{MAJOR}.{MINOR}.{PATCH}`
- [ ] `CHANGELOG.md` updated with all changes since last release
- [ ] Release notes published in GitHub Releases
- [ ] `main` CI pipeline passes completely

---

## DoD Enforcement

| Mechanism                           | What It Enforces                                   |
| ----------------------------------- | -------------------------------------------------- |
| GitHub branch protection            | Requires CI pass + 1 approval before merge         |
| `pyproject.toml` coverage threshold | Blocks test run if coverage < 90%                  |
| `pre-commit` hooks (optional)       | Run `black`, `isort`, `flake8` before every commit |
| PR template                         | Checklist appears automatically on every new PR    |
| Sprint Review ceremony              | Product Owner verifies acceptance criteria         |

> **Principle:** The DoD is non-negotiable. "Almost done" is not done.
> If a checklist item cannot be met, it must be raised in the Daily Standup immediately.
