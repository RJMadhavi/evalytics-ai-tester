# Capacity rules for test automation

**Why this file exists:** the owner's condition for testing Evalytics is that the automation must not impact server
capacity. There is no staging environment, so everything runs against the live site (own QA academies only).
These rules keep every run slow, gradual and easy to stop.

**Status:** the numbers below are proposals until the owner confirms them in writing. The server's real capacity is
unknown. The load target is **up to 500 students**, but the maximum actually allowed is whatever the owner confirms,
and every step up has to earn its place by the step before it being clean.

## To confirm with the owner

| Item | Proposed | Owner's answer |
|---|---|---|
| Maximum concurrent test students | Target 500, reached gradually | |
| Steps above 100 | Each one needs his explicit "go" for that run | |
| Quiet hours for bigger runs (IST) | late night / early morning | |
| Who can stop a run, and how to reach them | | |
| Can he watch server load (CPU, memory, response times) during steps above 100? | Yes, preferred | |
| Seat limit raised to 500, or bulk creation of students by him | | |
| Allow-listing of the load tool's IP address, if bot protection or rate limiting exists | | |

## Rules for all automation

| Area | Rule |
|---|---|
| UI suite (Playwright) | One browser at a time (`workers: 1`, no parallel files). At most one retry per test. No loops. Own academies only. |
| API checks | At most 2 requests per second. Stop a script after 3 errors (5xx or 429) in a row. |
| Agents | One agent at a time. At most 30 steps and 10 minutes per charter. At least 3 seconds between actions. No crawling outside own academies. |
| Change detection | At most once a day, at most 20 page loads. |
| Two suites at once | Never. Finish one before starting the next. |
| Real exams | Never run anything bigger than a single user while a real exam may be running. Ask the owner for the exam schedule or quiet hours. |
| Nightly or scheduled runs | None until the owner has agreed to the schedule in writing. |

## Load tests

**How the load is made.** With k6 at protocol level (HTTP requests that copy a student's login, exam load, answers,
auto-save and submit), not with 500 real browsers. Playwright is only used to capture what a real student does.
One laptop can generate this much light traffic, but all of it comes from one IP address, so the owner may need to
allow-list it.

**Students.** Up to 500 synthetic students (`loadtest-sNNN`) in dedicated academies (`eva-load-<n>`). Best case: the owner
bulk-creates them. Otherwise create them by script slowly, about one every 2 seconds, which is roughly 17 minutes for 500.
New students need owner approval, so plan for that step too. Handle email first: a catch-all test domain, or emails
switched off for these academies (ADR-0002).

**Steps (concurrent students).**

| Phase | Steps | Before each run |
|---|---|---|
| 1 | 10, 25, 50, 100 | Owner told (time, number, expected length). Written limits confirmed. |
| 2 | 150, 200, 300, 400, 500 | Owner gives an explicit "go" for that run, and watches server load if he can. Quiet hours only. |

**Each step.** Ramp up over 2 to 3 minutes, hold for 5 minutes, ramp down. Virtual students wait 5 to 10 seconds
between actions. Run one step at a time, with a maximum run time set in the script itself.

**The maximum is set in one place.** The script reads `MAX_VUS` and defaults it to 25. Raise it only after the owner's
written confirmation names the new number, and record the change in the run log.

**Gate before moving up a step.** Go up only if all of these held for the whole step:

- p95 response time is at most 1.5 times the same-day baseline,
- error rate (5xx and timeouts) is under 0.5%,
- every auto-save and submit succeeded, and scores are correct (no lost or duplicated answers),
- the owner has not asked to stop.

If any of these fail, stay at that step or go back down. Do not try the next one.

**Abort immediately if** p95 response time is more than double the baseline, the error rate passes 1%,
anything visible breaks for a real user, or the owner asks.

**Baseline first.** One user, 10 loads each of the login page, dashboard, exam page and results page. Record the median and
p95. Repeat on the day of every load run.

**Deadline surge** (everyone submits in the same minute) is a spike, not a gradual ramp. It runs only at steps the owner has
approved separately for that purpose.

**What the result means.** On a live site with real users, the ladder may stop well before 500. That is a valid result:
the report states the highest clean step and why the next one was not attempted. It does not claim to show the server's limit.

## Stress tests

Not run. They are meant to push the system until it breaks, which conflicts with the owner's condition,
and there is no staging environment. Revisit if a staging instance becomes available (ADR-0002).

## Kill switch

- Browser or API runs: `Ctrl+C` in the terminal, or close the terminal window.
- k6: `Ctrl+C`, plus a maximum duration set in the script.
- Agents: step and time caps in the agent harness, plus `Ctrl+C`.
- The owner can ask me to stop at any time, and I stop immediately.

## Run log

Every run above a single user is recorded in `reports/runs/<date>/`: start and end time (IST), tool, number of
students, step sizes, `MAX_VUS`, response times, errors, gate result, and whether it was aborted. The owner can compare this
with his server graphs.
