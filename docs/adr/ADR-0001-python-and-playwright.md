# ADR-0001: Defer AI-feature testing

- **Status:** Accepted
- **Date:** 2026-11-27
- **Deciders:** Madhavi Joshi (project owner)
- **Affects:** modules M05, M06, M07, M13, M14; epics E10, E11; agent stage A4; sprint S5

## Context

Five modules depend on Evalytics AI features: PDF/DOCX question extraction (M05), AI explanations (M06),
the equation converter (M07), the Genie assistant (M13) and AI-translated exams (M14).

- The trial tenant allows only 5 uploads, 5 AI generations and 5 Genie questions. The test plan (section 5.3, "Budget")
  already notes this is too small for a statistically useful evaluation.
- A proper evaluation needs a golden PDF corpus, scorers and extra quota, which costs time the project is trying to save.
- Questions can be added to the question bank by hand, so the exam flows (paper builder, scheduling, exam taking,
  results) do not depend on any AI feature.

## Decision

AI-feature testing is **out of scope for now, by choice**.

1. M05, M06, M07, M13 and M14 are marked `scope: skipped` in `docs/modules.yaml`, with this ADR as the reason.
2. Test questions are entered manually: a hand-made set of about 20 questions with a known answer key.
3. Scripts and agents must never use upload, AI generation or Genie. This is written into the agent guardrails.
4. The AI test strategy (plan section 5.3) stays in the plan, marked deferred, for when AI testing is re-enabled.
5. Agent stage A4 is re-scoped to oracle agents that check deterministic outputs (scoring, results, analytics)
   against hand-calculated answer keys.

## Consequences

- **Untested, and reported as untested (not as passed):** extraction accuracy, the "under 10 seconds" extraction claim,
  explanation correctness, equation conversion, Genie accuracy and its hallucination and data-leak risk
  (rated P1 in the plan), and translation quality.
- Tenant isolation (M18) is still tested through the normal UI and API. Isolation through Genie is not tested.
- The full-plan estimate drops by 52 hours (E10: 40 h, E11: 12 h), from about 518 h to about 458 h.
- The final report must list the five modules in an "Untested areas" section. `scripts/coverage_check.py` prints this list.

## Alternatives considered

- **Test with the trial quota only.** Rejected: 5 samples per feature cannot support any conclusion.
- **Ask the owner for extra quota now.** Deferred: it adds waiting time and cost. Revisit after the baseline.

## Revisit when

The owner grants extra quota, or the scripted baseline is complete and time is available.
