# Test plan and README changes for v0.2.0

Date: 2026-11-27. Decisions: [ADR-0001](../adr/ADR-0001-defer-ai-feature-testing.md),
[ADR-0002](../adr/ADR-0002-load-and-stress-testing-under-authorization.md),
[ADR-0003](../adr/ADR-0003-fast-track-schedule.md).

This file is a working guide and, once merged, the change record. Search for the quoted text in your repo copy.
If the wording differs slightly in your newer copy, keep the meaning and apply the same change.
Do the parts in order: C first (authorization), then A (plan), then B (README), then D (board).

## What changes, in four lines

1. AI features (M05, M06, M07, M13, M14) are out of scope for now.
2. Performance, load and stress testing are in scope, under written authorization (stress on staging only).
3. The ten sprints are compressed into four bursts (about 147 h, about 19 working days).
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

## Part A: Edits to TEST-PLAN.md

**Why:** the plan is the project's contract. If it still says AI testing is planned and load testing is a non-goal,
the repo contradicts the work actually being done.

### A1. Front matter

Find `version: 0.1.0-draft`. Replace with `version: 0.2.0-draft`.
After the `created:` line add `updated: 2026-11-27`.

### A2. Section 1, non-goals

Find the line starting `**Non-goals:**`. Replace the whole line with:

```text
**Non-goals:** Stress testing against production, destructive or denial-of-service testing, testing third-party services (email, payment gateway) beyond integration touchpoints, and AI-feature testing for now (ADR-0001). Load and performance testing are in scope under written authorization (ADR-0002); stress testing runs on staging only.
```

### A3. Section 2, guardrails

Add these checklist items at the end of the list:

```text
- [ ] Extend `docs/governance/AUTHORIZATION.md` with an addendum naming performance, load and stress testing (environment, maximum concurrent students, time window, stop rule). No load or stress test starts before the owner confirms it in writing.
- [ ] Load-test students live only in dedicated academies (`eva-load-<n>`), use synthetic names (`loadtest-sNNN`), and are listed in a CSV so the owner can delete them afterwards.
- [ ] Bulk-created students use a mail domain I control with a catch-all inbox, or the owner switches off emails for the load-test academies.
```

In the existing bullet starting `Agent guardrails:` add at the end: `Agents never use upload, AI generation or Genie (ADR-0001).`

### A4. Section 3.2, feature inventory

Add this paragraph just above the table:

```text
`docs/modules.yaml` is the source of truth for module scope and priority; this table is a summary. As of v0.2.0, M05, M06, M07, M13 and M14 are out of scope by choice (ADR-0001).
```

Append ` (out of scope, ADR-0001)` to the module name in the rows for M05, M06, M07, M13 and M14.

### A5. Section 3.3, early observations

- In item 5 (marketing claims) add at the end: `Not verified in v0.2.0: the "under 10 seconds" extraction claim (M05 deferred).`
- In item 6 (Genie risk) add at the end: `Genie testing is deferred (ADR-0001), so this risk stays untested.`

### A6. Section 4, scope

- In 4.1 replace `light performance and resilience` with `performance and load testing (stress on staging only)`.
- In 4.1 remove `AI output quality, i18n/L10n`.
- In 4.2 add at the end: `AI features M05, M06, M07, M13, M14 (deferred by choice, ADR-0001) and stress testing against production.`

### A7. Section 5.1, risk table

- On the rows `Genie data access and grounding` and `AI extraction accuracy`, append to the Rationale cell: ` Deferred (ADR-0001).`
- On the row `Multilingual rendering and translation`, append the same.
- Add a new row (priority is my proposal; adjust if you disagree):

```text
| Exam-taking performance under concurrent load | High | Medium | **P1** | A whole class starts at once; slow or failed saves cause disputes |
```

### A8. Section 5.2, test levels table

- Row `AI quality`: change the Technique cell to `Deferred (ADR-0001)`.
- Row `i18n`: change the Technique cell to `Deferred (M14 out of scope)`.
- Row `Performance (light)`: rename to `Performance, load and stress`. Technique: `Page-load budgets; ramped load tests on the exam flow under written authorization; stress on staging only`. Tooling: `Lighthouse, k6`.

### A9. Section 5.3, AI feature test strategy

Add this note directly under the heading:

```text
> **Deferred in v0.2.0 (ADR-0001).** This section is kept as the strategy for when AI testing is re-enabled. Do not run these tests against the trial quota.
```

### A10. Section 6, agents

- In the 6.2 table, replace the A4 row with:

```text
| A4 | **Oracle agents:** Agents verify deterministic outputs (scoring, results, analytics) against hand-calculated answer keys. AI-feature oracles (Genie, extraction) are deferred (ADR-0001) | Metrics dashboard produced per run |
```

- In 6.3, in the Guardrails bullet, add `no upload, AI generation or Genie` to the action allow-list.

### A11. Section 7, environment and data

- Tenants row: add `; load-test academies eva-load-<n>.evalytics.in, created only after the authorization addendum is confirmed`.
- Accounts row: add `; load-test students loadtest-sNNN created in small batches and listed in a CSV`.
- Email row: add `; a catch-all domain for bulk accounts`.
- Data row: replace `Golden PDFs.` with `Hand-made 20-question set with answer key (golden PDFs deferred).`

### A12. Section 9, estimates

Change these rows, then recompute the totals:

| Epic | Old | New | Note |
|---|---:|---:|---|
| EVA-E10 AI feature quality | 40 | 0 | Deferred (ADR-0001) |
| EVA-E11 Multilingual / i18n | 12 | 0 | Deferred (ADR-0001) |
| EVA-E13 | 18 | 18 | Rename to "Performance, load and stress (authorized)" |

New subtotal: 450 - 40 - 12 = **398**. Contingency 15%: **60**. New total: **about 458 h**.
Add a line under the table: `Seeding load-test students is part of E04. Re-baseline after Sprint 0.`

### A13. Section 9.1, duration table

Replace the table with:

| Weekly productive hours | Calendar duration | 2-week sprints |
|---:|---:|---:|
| 15 h (side project) | ~31 weeks | ~16 |
| 20 h | ~23 weeks | ~12 |
| 30 h | ~15 weeks | ~8 |
| 40 h (full-time) | ~12 weeks | ~6 |
| Fast-track (147 h) at 40 h | ~4 weeks | n/a (see 9.4) |
| Fast-track (147 h) at 20 h | ~7 weeks | n/a (see 9.4) |

### A14. New section 9.4, fast-track variant

Add after 9.3:

```text
### 9.4 Fast-track variant (ADR-0003)

Target: about 147 h, about 19 working days at 8 h/day. Estimate accuracy about plus or minus 30%.

| Epic | Hours |
|---|---:|
| E01 | 3 |
| E02 | 6 |
| E03 | 8 |
| E04 | 7 |
| E05 | 16 |
| E06 | 10 |
| E07 | 20 |
| E08 | 6 |
| E09 | 10 |
| E10 | 0 (deferred) |
| E11 | 0 (deferred) |
| E12 | 5 |
| E13 | 14 |
| E14 | 14 |
| E15 | 6 |
| E16 | 3 |
| **Subtotal** | **128** |
| Contingency (15%) | 19 |
| **Total** | **about 147** |
```

### A15. Section 10, sprint roadmap

- Mark the AI-feature evaluation row (S5 in your copy) as `Deferred (ADR-0001)`.
- Make the order match the README: load and stress testing is S7, agents A1-A3 is S8, agents A4-A5 is S9.
- Add this note under the table:

```text
Fast-track (ADR-0003): sprints are compressed into four bursts. Burst 1 = S0 and the start of S1 (days 1-5). Burst 2 = S1-S3 (days 6-10). Burst 3 = S4-S7, trimmed (days 11-15). Burst 4 = agents and wrap-up (days 16-19).
```

### A16. Section 11, exit criteria

- Replace the bullet `AI-feature metrics reported with sample sizes and confidence notes` with: `AI features deferred (ADR-0001); the final report lists M05, M06, M07, M13 and M14 as not tested`.
- Add: `Load results reported with ramp levels, environment, and evidence that the stop rule was respected`.

### A17. Section 14, risks

Add two rows:

```text
| Load or stress testing degrades production for real users | Med | High | Staging; written approval; gradual ramp; stop rule; agreed off-peak window; owner informed |
| Bulk student creation floods real email | Med | Med | Catch-all test domain, or owner switches off emails for load-test academies |
```

Also add both to `docs/risk-register.md`.

### A18. Section 15, open questions

Add:

```text
8. Which environment may load tests run on, with what maximum concurrent students, in which time window?
9. Can the test tenant's seat limit be raised, and is there a bulk student import or seed route?
10. Can emails be switched off for load-test academies?
11. Does the owner allow stress testing on staging?
```

Question 1 (staging) now also decides whether the stress test day happens at all.

### A19. Section 17, revision history

Add a row:

```text
| 0.2.0 | 2026-11-27 | Madhavi Joshi | AI features deferred (ADR-0001); load, performance and stress testing in scope under authorization (ADR-0002); fast-track schedule (ADR-0003); modules.yaml added |
```

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
