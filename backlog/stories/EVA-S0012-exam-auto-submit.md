---
id: EVA-S0012
type: story
epic: EVA-E07
title: Student exam auto-submits at deadline
status: Backlog          # Backlog | Ready | In Progress | In Review | Done | Won't do
priority: P0
estimate_hours: 5        # most likely
estimate_range: [3, 9]   # optimistic, pessimistic
sprint: null
labels: [exam, timing, automation]
covers: [M09, M10]
links: { blocks: [], depends_on: [], tests: [] }
---

## Description

As a student, when the exam window closes my answers are submitted automatically,
so I do not lose my work if I forget to press Submit.

## Acceptance Criteria

- [ ] Given an exam ending at T, when T passes, then the attempt is submitted with the answers saved so far
- [ ] A 10-minute warning is shown at T-10m
- [ ] A submit attempt after T is rejected with a clear message
- [ ] The result page shows a score based on the answers that were saved before T

## Test Notes

- Use a short window (for example 12 minutes) in the QA tenant.
- Verify against **server time**, not the browser clock. Also try once with the computer clock set wrong.
- Start this test early in the day: it needs real waiting time. Work on something else while it runs.
- Use a hand-made question set with a known answer key so the expected score is already calculated.
- Do not use any AI feature (upload, explanations, Genie) in this story.

## Notes

IDs `depends_on` and `tests` are empty on purpose. Fill them in once the task and test case files exist.
If `EVA-S0012` is already used in `backlog/stories/`, renumber this file and the `id` above.
