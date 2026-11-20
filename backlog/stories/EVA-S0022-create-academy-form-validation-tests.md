---
id: EVA-S0022
type: story
epic: EVA-E07
title: Create academy form validation tests
status: Ready
priority: P1
estimate_hours: 5
estimate_range: [3, 8]
sprint: null
---
## Description
As the QA engineer, I want automated negative tests of the sign-up form, so bad input is rejected.

## Acceptance Criteria
- [ ] tools/dump_form.py output reviewed and the page object uses the real field locators
- [ ] Cases cover empty fields, bad subdomain characters, mismatched passwords and an invalid email
- [ ] Every case passes require_invalid_academy_form() before submitting, so no real academy can be created
- [ ] Needs the owner's written approval for form submissions before the first run
