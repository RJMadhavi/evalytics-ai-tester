---
id: EVA-DOC-002
title: Testing Authorization and Scope
status: Draft (not valid until confirmed by the owner)
related: EVA-S0003
---

# Testing Authorization and Scope

This repository is public. **Do not paste the owner's email address, phone number, login details or the original message here.** Keep the evidence privately (see section 9) and refer to it by date and subject only.

## 1. Parties

| Role | Name |
|------|------|
| Application owner (authorizing) | BalkrishnaJ, <role/company> |
| Tester | MadhaviJ |
| Stop contact (can halt any test, any time) | <name>, reachable by <channel, not published here> |

## 2. System under test

- Application: Evalytics, https://evalytics.in
- Version observed: v1.1.0 (the footer version is recorded on every test run)
- Environments covered: <Production own-tenant only / Staging at ... / both>
- Tenant(s) the tester may use: `<qa-tenant-name>.evalytics.in` and a second tester-controlled tenant for isolation checks

## 3. Validity

- Start date: <2026-11-18>
- End date: <2026-11-18>
- Renewal: by written confirmation from the owner. Testing stops at the end date.

## 4. Permitted test types

Fill in each row with **Yes**, **No** or **Yes, with limits**.

| Test type | Permitted? | Limits and notes |
|-----------|-----------|------------------|
| Functional and exploratory testing | | Own tenant only |
| Automated UI testing | | Throttled, see section 5 |
| API testing | | Own tenant only |
| Accessibility testing | | |
| AI feature testing (extraction, explanations, Genie, translation) | | Within the AI quota granted in section 6 |
| Security testing, passive (observing traffic, checking headers and cookies) | | |
| Security testing, authentication and lockout (wrong-password attempts) | | Own accounts only, maximum <N> attempts |
| Security testing, authorization and tenant isolation (cross-tenant access attempts) | | Only between two tenants the tester controls |
| Load testing | | Staging preferred, see section 5 |
| Stress testing | | Staging only, see section 5 |
| AI-agent testing | | Allow-listed domain, throttled, kill switch |

## 5. Limits and rules

| Item | Limit |
|------|-------|
| Request rate for automated tests | <N> requests per second at most |
| Load test maximum virtual users | <N> |
| Stress test maximum virtual users | <N> |
| Allowed time windows for load and stress | <days and times, with time zone> |
| Environment for load and stress | <staging / production only when no real exams are running> |

**Always forbidden:** denial-of-service attempts aimed at harming the service, accessing or changing other tenants' real data, deleting or changing real users' accounts, spam, using real students' details, and social engineering of staff or users.

**Stop rules:** testing stops immediately if the stop contact asks, if error rates or response times pass the agreed ceiling, or if any real user reports a problem that may be caused by testing.

## 6. Quotas and costs

- AI usage granted for evaluation: <uploads> uploads, <generations> AI generations, <questions> Genie questions
- Any plan upgrade or paid add-on: <agreed / not agreed>
- Costs: <who pays, if anything>

## 7. Data handling

- Only synthetic data is used. No real student data is accessed, stored or published.
- Test emails go to dedicated test mailboxes only.
- Credentials are kept in a password manager and never committed to this repo.
- Network captures (HAR files) are not committed, since they can contain session tokens.

## 8. Reporting and disclosure

- Security findings are reported privately to the owner first, and are not published in this repo.
- The owner has <number> days to respond before any redacted summary is published.
- Public write-ups remove tenant names, user details and exploitable specifics.

## 9. Evidence of authorization

- Evidence is stored privately at: <location, such as a private folder or password-protected archive>
- Reference: <date of the owner's message>, subject "<subject line>"
- The owner confirmed this scope on: <2026-11-18>

---

## 10. Authorization addendum (do this first)

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

## 11. Change log

| Date | Change | Confirmed by |
|------|--------|--------------|
| <2026-11-27> | Added additional auth. addendum | MadhaviJ |
