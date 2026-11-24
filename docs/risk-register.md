---
id: EVA-DOC-008
title: Risk Register
version: 1.0
status: Draft
updated: 2026-11-24
related: EVA-T0002
---

# Risk Register

Likelihood and impact use High, Med and Low. Review it at every sprint review and add, change or close rows.

## 1. Open risks

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|----|------|-----------|--------|------------|--------|
| R01 | Testing the live site affects real users | Med | High | Own academies only, read-only by default, about one page a second, a stop switch, heavy tests on a private copy or staging | Mitigated, watch |
| R02 | Written authorization and scope are not confirmed | Med | High | Scope email sent. Only read pages and use own academies until confirmed. Authorization file stays "not valid" until the owner replies. | **Open** |
| R03 | New test academies wait for manual approval, which blocks the owner, teacher and student walkthroughs | High | Med | Ask the owner to approve both. Use the existing academy meanwhile. Follow up after 48 hours. | **Open** |
| R04 | Connections from cloud machines (Codespaces, probably GitHub Actions) are dropped, so browser tests cannot run there | High | Med | Reachability check stops runs early. Run browser tests from another network. Ask the owner about allow-listing or a staging copy. | **Open** |
| R05 | The AI allowance in a trial academy (5 uploads, 5 generations, 5 Genie questions) is too small for a meaningful evaluation | High | Med | Ask for a higher allowance and a cost cap. Spend uploads on purpose. Do large runs on a private copy. | **Open** |
| R06 | Load and stress testing is not approved or has tight limits | Med | Med | Run them on a private copy or staging. Reduce to one scenario each if limits stay tight. | **Open** |
| R07 | Materials supplied privately for test design leak into the public repository | Low | High | Keep them out of Git and out of Codespaces on the public repo. Review each pull request's file list. Keep private findings in a private note. | Mitigated, watch |
| R08 | Findings are published before the owner has had time to fix them | Low | High | Report privately first, agree a fix window, redact tenant details in public write-ups | Mitigated |
| R09 | AI-agent results are unreliable (false alarms, run-to-run differences) | High | Med | Structured verdicts, evidence for every claim, a triage step, replay logs, comparison with scripted tests | Planned |
| R10 | The application changes during the project (v1.1.0 to later) | High | Med | Tag every run with the footer version and a sitemap snapshot, keep locators accessible and stable | Planned |
| R11 | One person does all the work, so illness or other commitments delay everything | Med | Med | Keep sprints at about 80% of capacity, keep the plan in Git, move unfinished items openly | Open |
| R12 | Too many items in progress at once, so little gets finished | Med | Low | Work-in-progress limit of three, one story at a time | Open |
| R13 | An earlier automation branch (PR #1) conflicts with the current structure | Med | Low | Parked as a draft. Review in a short spike before deciding what to keep. | Open |
| R14 | Email volume: exam schedules for many test students send many real emails | Med | Med | Ask the owner about switching notifications off in test academies. Use plus-addresses that land in test inboxes. | Open |
| R15 | Reported numbers or claims are wrong (for example a test count) | Med | Low | Check figures against CI before reporting them. Keep the claims register updated. | Open |

## 2. Closed or accepted risks

| ID | Risk | Outcome |
|----|------|---------|
| C01 | CI does not exist, so mistakes reach `main` | Closed: three checks run on every pull request |
| C02 | No safety rules for automated tests | Closed: shared guardrails with unit tests |

## 3. Review log

| Date | Change |
|------|--------|
| 2026-11-24 | Version 1.0 created at the end of Sprint 0 |
