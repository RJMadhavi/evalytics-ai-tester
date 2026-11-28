# ADR-0002: Load testing under capacity rules; stress testing deferred

- **Status:** Accepted. Load testing is conditional on written confirmation. Stress testing is deferred.
- **Date:** 2026-11-27
- **Deciders:** Madhavi Joshi (project owner)
- **Affects:** goals G3 and G4; epics E04, E13, E14; modules M09, M10 (exam under load); plan sections 2 and 5.5

## Context

Version 0.2.0 of the test plan already made load testing (G3) and stress testing (G4) goals, and section 2 requires written
owner approval and staging where possible. Three facts are now known:

1. The owner has given **verbal** approval. His condition: the automation must not impact server capacity.
2. There is **no staging environment**. Everything runs against the live site, which hosts real academies and students.
3. The real capacity of the server is unknown.

Bulk account creation also triggers real emails.

## Decision

| Type | Status | Where |
|---|---|---|
| Performance (one user) | In scope | QA academy |
| Load | In scope, gradual ladder up to a target of 500 students, within `docs/governance/CAPACITY-RULES.md` | Dedicated QA academies in production |
| Stress | **Deferred** | Needs staging; not run on production |

Conditions for any load run (these add to plan sections 2 and 5.5):

1. The owner's verbal approval is recorded in `docs/governance/AUTHORIZATION.md` (date, how it was given, what was said),
   and the load limits are confirmed by him in writing before the first load test. Everything that is not a load test
   can proceed meanwhile.
2. All automation follows `docs/governance/CAPACITY-RULES.md`: one browser at a time, throttled requests, a same-day
   baseline, a gradual ladder with a gate between steps, and abort rules relative to that baseline. The script's maximum
   (`MAX_VUS`) stays at 25 until the owner's written confirmation names a higher number. Steps above 100 each need his
   explicit go and, if he can, his eye on server load.
3. Load-test students live only in dedicated academies (`eva-load-<n>`), use synthetic names (`loadtest-sNNN`), and are
   recorded in a CSV. Accounts are created slowly, in small batches.
4. Emails are handled before accounts are created: a catch-all test domain, or the owner turns off emails for the academies.
5. No run happens while a real exam may be running. The owner is told before each run and can stop it.
6. The owner deletes the load-test academies and accounts afterwards. No script deletes accounts.

Tools: k6 (load scripts), Lighthouse (page speed), Playwright (to capture realistic flows).
AI endpoints are not load tested (plan section 5.5).

## Consequences

- Epic E14 (stress) is set to 0 hours. The full plan drops by 14 h more, to about 478 h with contingency.
- The target ceiling is 500 students, but the ladder stops at the first step that fails its gate, or at the maximum the owner
  confirms. The final report states the highest clean step and does not present it as the server's limit.
- On a live site with real users, reaching high steps can slow the service before an abort rule fires. That is why steps above
  100 need the owner's explicit go and quiet hours.
- The owner must raise the seat limit to 500 on the test tenant, or bulk-create the students, and may need to allow-list the load tool's IP.
- Risk register entries: automation uses server capacity; no staging; authorization is verbal only; bulk accounts flood email.

## Alternatives considered

- **Stress test production.** Rejected: it conflicts with the owner's condition and risks real users.
- **Skip load testing.** Rejected: exam-taking under a full class is a core product risk (P1 in plan section 5.1).
- **Wait for written approval before doing anything.** Rejected: only load tests depend on it.

## Revisit when

A staging environment exists, or the owner approves higher limits in writing.
