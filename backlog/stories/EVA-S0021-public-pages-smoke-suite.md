---
id: EVA-S0021
type: story
epic: EVA-E07
title: Public pages smoke suite
status: Ready
priority: P1
estimate_hours: 4
estimate_range: [3, 6]
sprint: null
---
## Description
As the QA engineer, I want read-only checks of the public pages, so I notice breakage and version changes early.

## Acceptance Criteria
- [ ] Home, pricing, login and create-academy load, show an Evalytics title and a footer version
- [ ] No console errors and no known tracker hosts on any public page
- [ ] Run summary written to reports/runs/<date>/ui-summary.json
- [ ] Suite runs green three times in a row
