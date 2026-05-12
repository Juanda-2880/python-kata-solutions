# Agile / Scrum Workflow — EPAM engX Integration

> This document describes how Agile/Scrum ceremonies and practices integrate with
> EPAM engX engineering discipline in the `python-kata-solutions` project.

---

## 1. Team Structure

```
┌─────────────────────────────────────────┐
│             Scrum Team                  │
│                                         │
│  Product Owner      Scrum Master        │
│  (backlog priority) (ceremony lead)     │
│                                         │
│  Development Team                       │
│  ├── Senior Engineer (tech lead)        │
│  ├── Engineer (implementation)          │
│  └── QA Engineer (test strategy)        │
└─────────────────────────────────────────┘
```

---

## 2. Sprint Structure

**Sprint Duration:** 2 weeks  
**Velocity Target:** 13–18 story points per sprint

```
Week 1, Day 1          Week 1, Day 5       Week 2, Day 5
     │                      │                   │
     ▼                      ▼                   ▼
Sprint Planning ──── Mid-Sprint Sync ──── Sprint Review
     │                                    Sprint Retro
     ▼                                         │
Daily Standups (every morning, 15 min)         ▼
     │                                   Next Sprint
     ▼                                    Planning
Backlog Refinement
(Wednesday, Week 1, 1 hr)
```

---

## 3. Ceremonies

### 3.1 Sprint Planning

**When:** First Monday of each sprint, 2 hours  
**Inputs:** Prioritised product backlog, team velocity, Definition of Done  
**Outputs:** Sprint backlog with committed stories and tasks

**Agenda:**

1. Product Owner presents top-priority stories (30 min)
2. Team clarifies acceptance criteria (30 min)
3. Engineers decompose stories into Technical Tasks (30 min)
4. Team commits to sprint scope based on velocity (30 min)

**engX Alignment:**

- Stories must be **INVEST** compliant (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Technical Tasks must include testing and documentation as explicit tasks, not afterthoughts
- No story is accepted into the sprint without defined Acceptance Criteria

### 3.2 Daily Standup

**When:** Every morning, 15 minutes, time-boxed strictly  
**Format:** Walking the board (not the team)

Each team member answers:

- What did I complete since last standup?
- What will I complete today?
- Is there any impediment?

**engX Alignment:**

- Impediments are escalated immediately, not parked
- "Almost done" is tracked as in-progress, not done
- CI failures are impediments and are treated with urgency

### 3.3 Backlog Refinement

**When:** Wednesday of Week 1, 1 hour  
**Inputs:** Raw backlog items from Product Owner  
**Outputs:** Refined, estimated, acceptance-criteria-complete stories for future sprints

**Activity:**

- Team reviews upcoming stories together
- Engineers raise technical concerns and unknowns
- Stories are sized using **story points** (Fibonacci: 1, 2, 3, 5, 8, 13)
- Stories > 8 points are split before acceptance into a sprint

### 3.4 Sprint Review (Demo)

**When:** Last Friday of each sprint, 1 hour  
**Audience:** Stakeholders, Product Owner, Scrum Team

**Format:**

1. Team demonstrates working software against Acceptance Criteria
2. Product Owner accepts or rejects each story
3. Stakeholders provide feedback
4. Backlog is updated based on feedback

**engX Alignment:**

- Only software that meets the full DoD is demonstrated
- Demonstrations use the actual running system, not slides
- Rejected stories are returned to the backlog with documented reasons

### 3.5 Sprint Retrospective

**When:** Last Friday of each sprint (after Review), 1 hour  
**Format:** Start / Stop / Continue

| Category     | Meaning                         |
| ------------ | ------------------------------- |
| **Start**    | Practices we should adopt       |
| **Stop**     | Practices that are hurting us   |
| **Continue** | Practices that are working well |

**Outputs:** 1–3 actionable improvement items, assigned, with a due date  
**engX Alignment:** Engineering metrics (coverage trends, CI failure rate, PR cycle time) are reviewed as data inputs

---

## 4. Backlog Management

### Priority Tiers

| Priority | Label       | Meaning                           |
| -------- | ----------- | --------------------------------- |
| 1        | `critical`  | Blocks release or other stories   |
| 2        | `high`      | Must be in current or next sprint |
| 3        | `medium`    | Scheduled in upcoming sprints     |
| 4        | `low`       | Nice-to-have, reviewed quarterly  |
| —        | `tech-debt` | Flagged for explicit scheduling   |

### Story Sizing Reference

| Points | Complexity       | Example                                 |
| ------ | ---------------- | --------------------------------------- |
| 1      | Trivial change   | Update a docstring, fix a typo          |
| 2      | Small feature    | Add a utility method to existing class  |
| 3      | Standard feature | Implement a new function with tests     |
| 5      | Moderate feature | New module with full test coverage      |
| 8      | Large feature    | Cross-cutting concern (logging, config) |
| 13     | Epic-level       | Must be split before sprint entry       |

---

## 5. Development Workflow (Branch Lifecycle)

```
1. Pick story from Sprint Board → move to "In Progress"
2. Create branch from develop:
       git checkout develop && git pull
       git checkout -b feature/US-001-dictionary-class

3. Implement in small, focused commits:
       git commit -m "feat(dictionary): add newentry() with type validation"
       git commit -m "test(dictionary): add unit tests for newentry()"
       git commit -m "docs(dictionary): add Google-style docstrings"

4. Push and open Pull Request → move story to "In Review"
5. Peer review → address feedback
6. CI passes → 1 approval → merge to develop
7. Move story to "Done" only when DoD is fully satisfied
```

---

## 6. Kanban Board Columns

```
┌──────────┬────────────┬────────────┬───────────┬──────────┐
│ Backlog  │  To Do     │ In Progress│ In Review │   Done   │
│          │ (Sprint)   │            │  (PR)     │          │
├──────────┼────────────┼────────────┼───────────┼──────────┤
│ US-005   │ US-004     │ US-003     │ US-002    │ US-001   │
│ US-006   │            │            │           │          │
└──────────┴────────────┴────────────┴───────────┴──────────┘
```

**WIP Limits:**

- In Progress: max 2 per engineer
- In Review: max 3 total (PRs stale > 24h trigger a standup flag)

---

## 7. Metrics & Continuous Improvement

The team tracks these engineering metrics every sprint:

| Metric                 | Target                        | Tool                   |
| ---------------------- | ----------------------------- | ---------------------- |
| Sprint velocity        | Within ±20% of target         | Jira / GitHub Projects |
| CI pass rate           | > 95% of builds green         | GitHub Actions         |
| PR cycle time          | < 24 hours from open to merge | GitHub Insights        |
| Test coverage          | ≥ 90%                         | pytest-cov             |
| Code review turnaround | < 4 business hours            | GitHub                 |
| Escaped defects        | 0 per sprint                  | Bug tracking           |

These are reviewed in the Retrospective and used to set targets for the next sprint.
