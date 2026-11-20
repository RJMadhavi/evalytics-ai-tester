---
id: EVA-DOC-005
title: Academy Flows Inventory
story: EVA-S0006
status: Template. Fill in while walking through the academy.
sut_version: v1.1.0
academy_alias: qa0
date: <2026-11-14>
---

# Academy Flows Inventory

A flow is one thing a user can do from start to finish, such as "owner approves a teacher". This document lists every flow in the academy you already have, so you can see what the app does, what each flow touches, and which flows are good first candidates for automation.

Nothing in this file is confirmed yet. The flow list in section 3 comes from the features the website advertises. Rename, delete or add rows as you find out what the app really does.

## 1. Ground rules

- **Your own academy only.** In this repo, call it `qa0`. Keep its real name and address out of Git.
- **Add it to the allow-list** for any automation: `EVA_ALLOWED_HOSTS="<your-academy-host>"` in your own terminal, never in a committed file.
- **Use test data only.** Made-up names, your test mailboxes, synthetic question files.
- **AI features have a small quota** (5 uploads, 5 AI generations, 5 Genie questions in a trial). Walk those flows last, and plan each use. Write down how many you have left after each one.
- **Some actions cannot be undone** (deleting, unenrolling, rejecting). Do these last, on throwaway test data.
- **Emails are real.** Any flow that sends mail goes to your test mailboxes. Note the sender, subject and arrival time.
- **Hold until the owner confirms in writing:** wrong-password lockout tests, access attempts across academies, bulk student creation, load or stress testing, and any agent run.
- **Screenshots:** crop out real names and faces. Never commit network captures (HAR files), which can contain session tokens.

## 2. How to record a flow

Copy one card per flow into section 5. Keep each card short.

```
### AF-00 <flow name>
Role:            owner | teacher | student
Entry point:     where you start (menu item, button, address path)
Preconditions:   what must exist first
Steps:
  1.
  2.
Result:          what you see when it works
Data created:    what is now stored (a batch, an invite code, an exam)
Emails sent:     sender, subject, arrival time, or "none"
Quota used:      AI uploads / generations / Genie questions used, or "none"
Can be undone:   yes | no | partly
Address paths:   the page addresses you passed through (path only, no ids)
Odd things:      error messages, slow steps, confusing wording
Screenshot:      docs/recon/screenshots/AF-00.png
```

To find address paths and which steps change data, open the browser's DevTools (Network tab) while you click. A step that sends a POST, PUT or DELETE changes data. Write the path, not the content, and never copy tokens or cookies.

## 3. Flow inventory

Confirm each row as you go. Touches: **E** sends email, **Q** uses AI quota, **D** deletes or cannot be undone, **$** involves billing.

| ID | Flow | Role | Module | Touches | Walk order | Status |
|----|------|------|--------|---------|-----------|--------|
| AF-01 | Log in as owner and log out | Owner | M02 | | 1 | |
| AF-02 | Tour the dashboard and main menu | Owner | M03 | | 2 | |
| AF-03 | View and edit academy settings (name, branding, language) | Owner | M01 | | 3 | |
| AF-04 | View plan, trial status and limits | Owner | M17 | $ | 4 | |
| AF-05 | View the activity log | Owner | M15 | | 5 | |
| AF-06 | Generate or view the student invite code | Owner | M04 | | 6 | |
| AF-07 | Add a teacher, then approve the teacher | Owner | M03 | E | 7 | |
| AF-08 | Teacher logs in through the teacher login | Teacher | M02, M03 | | 8 | |
| AF-09 | Create a batch or class | Owner or teacher | M04 | | 9 | |
| AF-10 | Student joins with the invite code | Student | M04 | E | 10 | |
| AF-11 | Approve or reject an enrollment request | Owner | M04 | E | 11 | |
| AF-12 | View the student list and a student's history | Owner or teacher | M11 | | 12 | |
| AF-13 | Add questions by hand to the question bank | Teacher | M05 | | 13 | |
| AF-14 | Set difficulty tags and edit a question | Teacher | M05 | | 14 | |
| AF-15 | Build a test paper manually | Teacher | M08 | | 15 | |
| AF-16 | Build a test paper by random pick (chapter and difficulty mix) | Teacher | M08 | | 16 | |
| AF-17 | Schedule an exam for a batch | Teacher | M09 | E | 17 | |
| AF-18 | Student takes an exam (answer, auto-save, submit) | Student | M10 | | 18 | |
| AF-19 | Results and analytics after the exam | Teacher, student | M11 | | 19 | |
| AF-20 | Student asks to re-attempt, teacher responds | Student, teacher | M12 | E | 20 | |
| AF-21 | Switch the exam language | Student | M14 | Q | 21 | |
| AF-22 | Upload a PDF and extract questions with AI | Teacher | M05 | Q | 22 | |
| AF-23 | View an AI explanation of a question | Teacher | M06 | Q | 23 | |
| AF-24 | Convert an equation to LaTeX | Teacher | M07 | Q | 24 | |
| AF-25 | Ask the Genie assistant a question | Owner, teacher | M13 | Q | 25 | |
| AF-26 | Send a bug report with a screenshot | Any | M16 | | 26 | |
| AF-27 | Unenroll a student with a reason | Owner | M04 | E, D | 27 | |
| AF-28 | Forgot password and reset | Any | M02 | E | 28 | |

Walk order: view-only flows first, then flows that create harmless data, then flows that send email, then AI quota, then anything that cannot be undone.

## 4. Questions to answer while you walk

- What does the owner see before any students exist, and after?
- How are teachers and students told apart in the menus?
- Does a student see a different page if they belong to two academies?
- Which screens show numbers you can later check against the data you entered (counts, averages, scores)?
- Which flows depend on a clock (windows, warnings, auto-submit)?
- Which pages work on a phone, and which do not?

## 5. Flow cards

Paste a card for each flow here as you finish it.

## 6. Automation candidates

Fill this in after you have walked the flows. A good first candidate is stable, reversible, free of email and AI quota, and checks something that matters.

| Flow | Risk (P0 to P3) | Stable? | Needs a write request? | Email or quota? | First candidate? |
|------|-----------------|---------|------------------------|-----------------|------------------|
| AF-01 | | | Yes (login) | | |
| AF-02 | | | | | |
| AF-05 | | | | | |

Rules of thumb:
- Read-only flows (AF-02, AF-05, AF-12, AF-19) work with the read-only guardrails as they are.
- Login and any create or edit flow needs `writes_ok`, which needs the owner's written approval first.
- Flows with **Q** are never part of a repeating test run, because the quota is small.
- Flows with **D** run only in a throwaway academy.

## 7. Findings log

| ID | Flow | What I saw | Expected | Evidence | Status |
|----|------|------------|----------|----------|--------|
| FLW-01 | | | | | |

## 8. Done criteria for S0006

- [ ] Every owner screen and menu item listed
- [ ] Flow cards written for AF-01 to AF-12 at least
- [ ] Walk order followed, and the AI quota left is recorded
- [ ] Anything surprising logged in section 7 as an unconfirmed finding
- [ ] Section 6 started so the first automation stories can be written
