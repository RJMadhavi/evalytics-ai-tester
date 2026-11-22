---
id: EVA-DOC-006
title: Source-Informed Test Design
status: Draft
related: EVA-S0006, EVA-S0020
---

# Source-Informed Test Design

This document turns what is known about how Evalytics is built into concrete tests. It describes **behaviour and test ideas only**. The application source code is private, is never committed to this repository, and is not quoted here. Security observations from reading the source are kept in a separate private note and are not part of this repo.

## 1. Test environments

| Environment | What runs there | Notes |
|-------------|-----------------|-------|
| Public site, own academy | Read-only checks, normal functional flows, small data | Needs the owner's written approval for anything that writes in bulk, floods, or probes security |
| **Private local instance** | Load, stress, security, tenant isolation, exam timing, Genie and rate-limit behaviour | Built from the private source on a private machine or private repo, with synthetic data and mocked AI keys. Tests reach it with `EVA_BASE_URL=http://localhost:<port>` |

Running the heavy and risky tests against a local instance removes most of the risk to real students, and most of the dependency on approvals. The local instance and its source never enter this public repo.

Needs for the local instance: Python 3.12, a database (PostgreSQL, or SQLite for light runs), a cache for rate limiting (an in-memory store is enough locally), mocked or switched-off AI calls, and seed data with two academies.

## 2. Product rules the tests should verify

| Module | Rule to verify | Layer | Where |
|--------|----------------|-------|-------|
| Academy creation | Academy name, subdomain, name, email and password are required | UI, API | Public (own), local |
| Academy creation | Subdomain is 3 to 60 characters: lowercase letters, digits and hyphens, starting and ending with a letter or digit | API | Local |
| Academy creation | Password has at least 8 characters, one capital letter and one digit, and must match its confirmation | UI, API | Public (own), local |
| Academy creation | One account per email address. A new academy stays inactive until approved. | API | Local |
| Academy creation | Reserved or look-alike subdomains (for example `www`, `admin`, `api`, `mail`) are refused | API | Local |
| Login | Wrong email or password gives one generic message | UI, API | Public (own) |
| Login | An account only works on its own academy's address, and the redirect after login stays on the same site | UI, API | Public (own), local |
| Login | Repeated bad attempts are limited. Check what the limit protects (one address, one account, everyone). | API | **Local only** |
| Sessions | Idle sessions end after a set time, and a logged-out session cannot be reused | API | Local |
| Roles | A student cannot open teacher pages, and a teacher cannot open student pages | UI, API | Public (own), local |
| Enrollment | Statuses are pending, approved, rejected, unenrolled. Only approved students can start an exam. | UI, API | Public (own), local |
| Question bank | Each question has options A to D, one correct option and a difficulty | UI, API | Public (own), local |
| Exams | Marks per right and wrong answer come from the test paper, or the subject if there is none (defaults 4 and -1) | API, unit | Local |
| Exams | Score = right × marks − wrong × penalty, unanswered = 0, rounded to 2 decimals (see `common/scoring.py`) | API, unit | Local, public (own) |
| Exams | Duration comes from the test paper, or the subject default if there is none | UI, API | Local |
| Results | Counts, score, percentage and the leaderboard match the reference scorer | API | Local, public (own) |
| Multi-academy | A student in two academies sees both, and each academy sees only its own data | UI, API | Local |
| Languages | English, Hindi, Marathi and Kannada switch the page and exam text | UI | Public (own) |
| Uploads | Only simple image names are served from the uploads path | API | Local |

## 3. Exam integrity tests (priority P0)

These tests protect the core promise that an exam ends on time and scores correctly.

1. **Late answers.** After the exam time has passed, saving an answer or submitting is refused by the server, not only by the page.
2. **Closed browser.** If a student closes the tab, the attempt is still ended and scored when time runs out, with the answers saved so far.
3. **Who says "auto".** The page tells the server whether a submission was automatic. A student must not be able to change that value or the submission time.
4. **Exam window.** A student cannot start an exam before the window opens or after it closes, and cannot restart a submitted exam.
5. **Double submit.** Two quick submissions produce one result and one email.
6. **Ownership.** One student cannot read, save to or submit another student's attempt.
7. **Bad input.** Saving with a missing body, a question from another exam, an invalid option letter or wrong data types is refused cleanly, never with a server error.
8. **Clock.** Timing uses server time. Changing the browser's clock changes nothing.
9. **Score.** For a spread of answer patterns (all right, all wrong, all blank, mixed, unusual marks), the score, counts and percentage equal the reference scorer.

## 4. Tenant isolation tests (priority P0)

Build a matrix of two academies, each with an owner, a teacher and a student, plus one student who belongs to both. For every page and data endpoint that takes an id (subjects, questions, tests, exams, results, assignments, batches, uploads, logs):

| Caller | Target | Expected |
|--------|--------|----------|
| Teacher A | Academy A's data | Allowed |
| Teacher A | Academy B's data by guessing ids | Refused or not found |
| Student A | Another student's attempt, in the same academy | Refused |
| Student A | Academy B's results and leaderboard | Not shown |
| Multi-academy student | Each academy | Sees only that academy's data in that academy's view |
| Anonymous | Any signed-in page | Redirected to login |
| Anyone | Another academy's address after logging in elsewhere | Logged out with a clear message |

Also check that public helper endpoints (anything callable without logging in) do not reveal who has an account or personal details. Run these on the local instance only.

## 5. Genie assistant tests (local instance only)

Genie turns a question into a database query. Test it as an exposed feature that can leak data:

- **Known answers.** A curated set of questions whose answers you compute independently, in one academy.
- **Scope.** Ask about other academies, "all students", every user, anything in the account tables, and check nothing from another academy or any credential-like column appears. Use two seeded academies with obviously different data.
- **Injection by data.** Put instructions into a student name, a batch name and a question text, then ask Genie about them. The instructions must be treated as data.
- **Rewording.** Ask the same forbidden thing in many phrasings, languages and formats.
- **Refusals.** Questions that need a write or a destructive action must be refused.
- **Resilience.** Very long questions, empty questions, and questions that produce huge results.

Record results with the model and settings used, because outputs vary between runs.

## 6. Reference scorer

`automation/common/scoring.py` is an independent oracle for exam results, with unit tests. A test submits a known set of answers, then compares the app's score, counts and percentage with the scorer's. A disagreement means either the app or the scorer is wrong, and the discussion of which is the test result.

## 7. Proposed new stories

Estimates are most likely hours and are added to the existing epics, not on top of them.

| Proposed story | Epic | Hours | Where |
|----------------|------|------:|-------|
| Local instance with two seeded academies (private) | E04 | 8 | Local |
| Reference scorer and unit tests | E08 | 2 | Done |
| Exam integrity tests (section 3) | E07 | 8 | Local |
| Tenant isolation matrix (section 4) | E10 | 10 | Local |
| Genie scope and injection tests (section 5) | E11 | 8 | Local |
| Claim checks: lockout, session, "tamper-proof" | E10 | 5 | Local |
| Rate-limit behaviour with a proxy in front | E10 | 4 | Local |
| Load and stress on the local instance | E13, E14 | 12 | Local |

These total about 57 hours, within the current 554-hour plan. Load, stress and security work now needs the owner's approval only for anything run against the live site.

## 8. Questions for the owner (safe to keep in the repo)

1. May the source be used to run a private local copy for testing, and may findings from reading it be reported to you privately?
2. Is there a staging copy of the live site?
3. Which version of the app does the live site run, and how are releases announced?
4. Who should receive findings, and what response time can be expected?
