# Sprint 0 Review

Sprint: S00, Nov 14 to Nov 27, 2026. Theme: foundations and recon. Held on: <date>.

## Goal

Have a working repo and board, written permission on file, a test academy with test accounts, and a written map of how the app behaves.

## Was the goal met?

**Partly.** The repo, board, CI and test framework are in place and working. Permission and the test academies depend on the owner and are not finished.

## What got done

| Item | Result |
|------|--------|
| EVA-S0001 Repo and folder structure | Done |
| EVA-S0002 GitHub Project board | Done |
| EVA-S0004 CI skeleton | Done, three green checks |
| EVA-S0009 Test mailboxes | Done |
| Public pages documented (S0005) | Documented, browser checks pending |
| Academy flows inventory (S0006) | Template ready, walkthrough in progress |

Work done beyond the Sprint 0 plan, pulled forward on purpose:

| Item | Result |
|------|--------|
| EVA-S0020 Automation scaffold with safety rules | Done, 14 unit tests |
| Reference scorer for exam results | Done, 8 unit tests |
| AI extraction scorer and four synthetic test papers | Done, 15 unit tests |
| Source-informed test design and AI testing strategy | Done |
| Site reachability check | Done, 5 unit tests |
| Risk register and this review | Done |

CI on `main`: 42 unit tests and three checks, all green.

## What did not get done, and why

| Item | Why | Moves to |
|------|-----|----------|
| EVA-S0003 Owner authorization | Waiting for the owner's reply | Sprint 1 |
| EVA-S0006 Walk through the owner flow | Only partly started, and the new academies are waiting for approval | Sprint 1 |
| EVA-S0007 Teacher and student flows | Needs approved test academies | Sprint 1 |
| EVA-S0008 Map network calls | Not started | Sprint 1 |
| EVA-S0010 Create test accounts | Needs approved test academies | Sprint 1 |
| EVA-S0005 browser checks | Cloud machine cannot reach the site | Sprint 1 |
| EVA-S0011 Ask the owner the open questions | Covered by the scope email and the progress update | Close as done when the reply arrives |

## Demo notes (what I would show)

1. The board with the sprint field and estimates.
2. A pull request with its three green checks, then the merge.
3. The test framework refusing a risky action: a blocked write and a blocked address (unit tests).
4. The AI scorer on a perfect and a damaged extraction.
5. The public page findings, with the confirmed ones marked.

## Planned hours against actual hours

| | Hours |
|---|------:|
| Planned for the sprint | 40 |
| Closed from the plan | <fill in from the board> |
| Pulled forward from later sprints | <fill in> |
| Total worked | <fill in> |

## What the sprint changed in the plan

- Automation and AI test tools are ahead of schedule.
- Owner-dependent items (authorization, academy approval, network access) are behind schedule, so they come first in Sprint 1.
- Heavy and risky tests move to a private copy or staging, which cuts the need for approvals.
- Cloud machines cannot reach the site, so browser tests run from another network until that is solved.
- Estimates: the total of about 554 hours stands. Hours move from approvals-dependent work to local-copy work.
