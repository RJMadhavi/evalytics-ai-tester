# ADR-0003: Fast-track schedule

- **Status:** Accepted
- **Date:** 2026-11-27
- **Deciders:** Madhavi Joshi (project owner)
- **Affects:** plan sections 9, 9.1, 9.4, 10; sprint structure

## Context

The full plan is about 554 hours in version 0.2.0, and about 478 hours after ADR-0001 defers AI functionality testing
and ADR-0002 defers stress testing. At 8 focused hours a day that is roughly 60 working days. The goal now is to finish as quickly as possible without
dropping the P0 risks.

## Decision

Compress the ten two-week sprints into **four bursts**, targeting about **151 hours (about 19 working days at 8 h/day)**.
Each epic is shrunk, not removed, except where another ADR defers it. The per-epic hours are in plan section 9.4.

| Burst | Covers | Days | Main outputs |
|---|---|---|---|
| 1 | S0 and the start of S1 | 1-5 | Authorization, tenants, feature map, 20-30 test cases, first Playwright test |
| 2 | S1-S3 | 6-10 | P0/P1 scripted flows, API notes, authentication security checks |
| 3 | S4-S7, trimmed | 11-15 | Tenant isolation, load testing within the capacity rules, browser and accessibility spot-checks (stress deferred, ADR-0002); load ladder up to 500 only as far as the owner approves |
| 4 | S8-S9 | 16-19 | Local-model agent runs compared with scripts, triage, short report |

Not negotiable even when rushing: written authorization, testing only the own tenant, throttled runs,
security findings kept private, and agents built last so scripted tests act as the answer key.

## Consequences

- Lower coverage of P2/P3 areas; no nightly agent run in CI; no burndown charts or retros.
- Estimate accuracy is about plus or minus 30%.
- A buffer and re-test day sits at the end of burst 3. Slow timed tests (such as auto-submit) are started early
  and run in the background.

## Alternatives considered

- **Run the full plan.** Rejected: too long for the stated goal.
- **One-week version (about 40 h).** Possible fallback: P0 items only, no agents.

## Revisit when

Sprint 0 recon changes the estimates, or the owner's answers (staging, quota, permitted tests) change the scope.
