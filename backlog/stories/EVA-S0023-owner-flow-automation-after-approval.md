---
id: EVA-S0023
type: story
epic: EVA-E07
title: Owner flow automation after approval
status: Ready
priority: P1
estimate_hours: 8
estimate_range: [5, 12]
sprint: null
---
## Description
As the QA engineer, I want automated checks of the owner dashboard, so regressions in academy management are caught.

## Acceptance Criteria
- [ ] Depends on EVA-S0003 (authorization) and the QA academies being approved
- [ ] Login as the QA owner, dashboard loads, main menu items reachable
- [ ] Credentials come from environment variables, never from Git
- [ ] Teacher approval and invite code flows covered once the app behaviour is documented in S0006
