---
id: EVA-S0020
type: story
epic: EVA-E06
title: Python Playwright scaffold with guardrails
status: Ready
priority: P1
estimate_hours: 6
estimate_range: [4, 9]
sprint: null
---
## Description
As the QA engineer, I want a test framework that cannot harm the live site, so I can automate safely.

## Acceptance Criteria
- [ ] automation/ folder with pytest, pytest-playwright and requirements committed
- [ ] Guardrails (allow-list, read-only by default, throttle, kill switch) implemented and unit tested
- [ ] Unit tests run in CI on every pull request
- [ ] ADR-0001 accepted and the test plan tooling table updated
