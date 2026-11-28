# Test plan and README changes for v0.3.0

Date: 2026-11-27. Decisions: [ADR-0001](../adr/ADR-0001-defer-ai-feature-testing.md),
[ADR-0002](../adr/ADR-0002-load-and-stress-testing-under-authorization.md),
[ADR-0003](../adr/ADR-0003-fast-track-schedule.md).

The plan in the repo was already at 0.2.0 (dated 2026-11-15), so these changes make it **0.3.0**.
This file is a working guide and, once merged, the change record.
Do the parts in this order: C (authorization), then A (plan), then B (README), then D (board).

## What changes, in four lines

1. AI features (M05, M06, M07, M13, M14) are out of scope for now (ADR-0001).
2. Load and stress testing were already goals G3 and G4. ADR-0002 adds the rules for student accounts, email and cleanup.
3. The ten sprints are compressed into four bursts (about 151 h, about 19 working days, ADR-0003).
4. `docs/modules.yaml` becomes the source of truth for module scope and priority.

---

## Part C: Authorization addendum (do this first)

**Why first:** load and stress tests can affect real users. Nothing in this addendum is approved until the owner
confirms it in writing. Do not fill in values on the owner's behalf and do not mark anything as approved yourself.

Add this section to `docs/governance/AUTHORIZATION.md`, send it to the owner, and store their reply
(for example under `docs/governance/evidence/`) before any load or stress run.

```text
## Addendum: performance, load and stress testing (requested 2026-11-27)

Status: REQUESTED, not yet approved.

Requested scope
- Performance checks (Lighthouse and similar) on pages in the QA academy.
- Load tests on exam-taking flows, ramped gradually, using synthetic students (loadtest-sNNN)
  in dedicated academies (eva-load-N).
- Stress tests: staging only.

To be filled in by the owner
- Environment:                 [ ] staging   [ ] production QA academies only
- Maximum concurrent students: ______
- Allowed window (IST):        ______ to ______ on ______
- Stop rule:                   stop if error rate exceeds ____% or p95 response time exceeds ____ s,
                               or whenever the owner asks
- Stress testing:              [ ] allowed on staging only   [ ] not allowed
- Emails for bulk accounts:    [ ] catch-all test domain   [ ] owner switches emails off for these academies
- Seat limit raised to:        ______
- Cleanup:                     owner deletes eva-load-N academies and loadtest accounts after the tests

Confirmed by: ______  Date: ______  Evidence (link or file): ______
```

---

## Part A: TEST-PLAN.md

**How:** upload the new `TEST-PLAN.md` over the existing one (same folder, same file name) on your branch.
GitHub shows it as a modified file. Open **Files changed** and check that only the sections below changed.
If other sections show changes, something differs from the copy I started from, so tell me before merging.

**Why:** 60 small edits across the file are easy to get wrong by hand. The replacement file was built from the
0.2.0 text you pasted, with each change applied once. Sections 5.4, 5.6, 5.7, 6.3, 8.3 and 12 are unchanged.

| Section | What changed |
|---|---|
| Front matter | `version: 0.3.0-draft`, `supersedes: 0.2.0-draft` |
| 1 Purpose and goals | G6 marked deferred; AI testing added to the non-goals; purpose line adjusted |
| 2 Guardrails | AI quota bullet replaced by "do not use AI features"; two new bullets for load-test academies and bulk email; agent guardrail extended |
| 3.2, 3.3 | `modules.yaml` note; M05, M06, M07, M13, M14 marked out of scope; two notes on unverified claims |
| 4 Scope | AI quality and i18n removed from in scope; AI modules added to out of scope |
| 5.1, 5.2, 5.3 | Genie, extraction and multilingual rows marked deferred; G6 row marked deferred; deferred note under 5.3 |
| 5.5 | One sentence on how load-test accounts are created and cleaned up |
| 6.2, 6.4 | A4 re-scoped to deterministic outputs; no upload, AI generation, Genie or translation in the agent action list |
| 7 Environment | Load-test academies, `loadtest-sNNN` accounts, catch-all email, hand-made question set |
| 8.1, 8.2 | `docs/modules.yaml` and `scripts/` added to the layout; "Won't do" column added to the board |
| 9 Estimates | E04 wording; E11 set to 0; subtotal 430 h, contingency 65 h, total about 495 h |
| 9.1 | Duration table recalculated; two fast-track rows added |
| 9.2 | Effort percentages marked approximate; AI share removed |
| 9.4 (new) | Fast-track variant: hours per epic (about 151 h) and the four bursts |
| 10 Roadmap | S5 marked deferred; S6 theme adjusted; fast-track note |
| 11 Exit criteria | AI metrics replaced by "listed as not tested" |
| 13, 14, 15, 16 | AI metrics marked deferred; two risks changed or added; two questions added and one reworded; `modules.yaml` mentioned |
| 17 Revision history | New 0.3.0 row; `<your-name>` replaced by MadhaviJ in the older rows |

Fast-track hours in 9.4 are my proposal, including 3 h for unit tests of the repo's scripts (goal G2).
Change them if you disagree, but keep the total in section 9.4 and in ADR-0003 in step.

---

## Part B: Edits to README.md

**Why:** the README is the first thing a reader sees. Right now it shows a broken badge, a broken link,
and plans that no longer match the work.

### B1. Fix the CI badge

The badge URL contains the placeholder `<your-username>`. Replace it with `RJMadhavi` in **both** places in that line:

```text
https://github.com/<your-username>/evalytics-ai-tester   ->   https://github.com/RJMadhavi/evalytics-ai-tester
```

Then confirm that `.github/workflows/ci.yml` exists. If the workflow file has another name, change the badge URL to match.

### B2. Fix the test-plan links

The README links the plan twice with different paths: `docs/test-plan/TEST-PLAN.md` and `docs/testplan/TEST-PLAN.md`.
Run `ls docs` to see which folder exists, then make both links use that path. Do not guess.

### B3. Goal 6

Find the line starting `6. **Testing the underlying AI functionality:**`. Replace with:

```text
6. **Testing the underlying AI functionality (deferred):** question extraction, explanations, equation conversion, translation and the Genie assistant. Out of scope for now by choice (see ADR-0001). The strategy stays in the test plan for when it is re-enabled.
```

### B4. Test approach bullet

Find the bullet starting `- **AI features:**`. Replace with:

```text
- **AI features (deferred):** non-deterministic output would be evaluated with golden datasets, rubric scoring and metamorphic tests rather than exact-match assertions. Not run for now (ADR-0001).
```

### B5. Agent roadmap, A4 row

Replace the A4 description `Oracle agents for AI features (Genie, extraction)` with:

```text
Oracle agents that check scoring, results and analytics against hand-calculated answer keys (AI-feature oracles deferred)
```

### B6. Project status table

- Change the S5 status from `Planned` to `Deferred (ADR-0001)`.
- Add this line under the table:

```text
Fast-track: the sprints are compressed into four bursts of about 19 working days in total (ADR-0003). Estimates are re-baselined after Sprint 0.
```

### B7. Repository layout block

In the layout code block add two lines, aligned with the others:

```text
docs/modules.yaml   Module list and scope (source of truth for coverage)
scripts/            Helper scripts, for example coverage_check.py
```

The repo also has top-level `ui/` and `common/` folders that the layout does not mention, and the layout shows `automation/ui/`.
Open each folder first. If `ui/` duplicates `automation/ui/`, decide which one stays. If both are intended, document both.
Do not move anything until you have checked whether open PR #1 touches those folders.

### B8. New section: out of scope for now

Add this section after "Test approach at a glance":

```text
## Out of scope for now

These modules are not being tested. They will be listed as untested in the final report, not as passed.

| Module | Reason |
|---|---|
| M05 Question bank (PDF/DOCX upload, AI extraction) | AI feature, deferred (ADR-0001) |
| M06 AI explanations | AI feature, deferred (ADR-0001) |
| M07 Equation converter | AI feature, deferred (ADR-0001) |
| M13 Genie AI assistant | AI feature, deferred (ADR-0001) |
| M14 Multilingual (AI-translated exams) | AI feature, deferred (ADR-0001) |

Run `python scripts/coverage_check.py` for the live list.
```

---

## Part D: Project board

**Why:** the board should show the same decisions as the files, so nobody has to guess what was skipped.

1. Add a status column **Won't do**.
2. Create five cards, one each for M05, M06, M07, M13, M14. Put them in Won't do and write "ADR-0001" in the card.
3. Add custom fields **Module** (M01-M18), **Priority** (P0-P3), **Burst** (1-4) and **Epic** (E01-E16).
4. Create the views **Board** (by Status), **By module** (table grouped by Module) and **Sprint** (grouped by Burst).
5. Create one story per in-scope module that has none yet, starting with the P0 gaps the script reports.
   Each story needs a `covers:` line so the coverage script can see it.
