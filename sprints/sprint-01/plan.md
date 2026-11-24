---
sprint: S01
theme: Baselines and the private test environment
start: 2026-11-28
end: 2026-12-11
capacity_hours: 40   # assumes 20 h/week, change it to your real number
committed_hours: 32
---

# Sprint 1 Plan

## Sprint goal

Get a first real baseline of the public pages and the AI extraction, finish the walkthroughs of the approved academy, and choose and prepare a safe place to run the heavy tests.

## Committed work (about 80% of capacity)

| ID | Title | Hours | Depends on |
|----|-------|------:|------------|
| EVA-S0003 | Record owner authorization | 1 | Owner reply |
| EVA-S0005 | Finish the public page browser checks | 2 | A network that reaches the site |
| EVA-S0021 | Public pages smoke suite, run and record the baseline | 3 | A network that reaches the site |
| EVA-S0006 | Walk through the owner flow (academy flows inventory) | 5 | Existing academy |
| EVA-S0008 | Map network calls in the own academy | 4 | Existing academy |
| EVA-SP0001 | Review the parked automation branch and decide | 2 | none |
| EVA-S0030 | AI extraction baseline: first paper through the app and scored | 4 | One AI upload |
| EVA-T0001 | Sprint ceremonies and notes | 4 | none |
| EVA-S0007 | Teacher and student flows | 4 | Approved test academies |
| EVA-S0010 | Create test accounts | 3 | Approved test academies |
| | **Committed** | **32** | |

The last two items only start if the test academies are approved. If not, they roll over and the hours go to the stretch items.

## Stretch (only if committed work is finished)

| ID | Title | Hours |
|----|-------|------:|
| New | Private test environment: choose where it lives and set it up | 8 |
| New | Exam integrity tests on the private environment | 8 |

## Rules for this sprint

- No more than three items In Progress.
- Every piece of work has an issue before it starts, and a pull request that links to it.
- A short weekly update to the owner.
- Figures reported anywhere are checked against CI or the board first.

## Definition of Done

- The item is merged through a pull request with green checks, or the document is committed with its checks green.
- Acceptance criteria are ticked and the issue is closed.
- Burndown and notes are updated.

## Risks to watch

R02 authorization, R03 academy approval, R04 network access, R05 AI allowance. See `docs/risk-register.md`.
