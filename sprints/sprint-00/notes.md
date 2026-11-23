# Sprint 0 notes

Short notes for task EVA-T0001. One entry per working session, newest at the bottom. Three lines is enough: what got done, what is blocked, what is next. Adjust the dates to match when things actually happened.

Keep these notes public-safe: no passwords, no real email addresses, no academy names or addresses, and nothing about security weaknesses.

## Template

```
## 2026-11-22
Done: 
Blocked: 
Next: 
Hours remaining: 30
Notes: 
```

## Week 1 (from Nov 14)

Done: repo, project board and sprint field set up (S0001, S0002). CI skeleton merged through a pull request, three green runs (S0004). Test mailboxes planned and created (S0009). Public pages documented (S0005, browser checks still open).
Blocked: owner authorization (S0003) and approval of the new test academies. Both are waiting on the owner.
Next: walk the flows of the existing academy (S0006) and finish the public pages browser checks.
Hours remaining: 30
Notes: a review of the first 14 days will show whether the approval wait pushed S0007 and S0010 into Sprint 1.

## Nov 21 to Nov 22

Done: automation scaffold merged with shared safety rules and unit tests (S0020), reference scorer added, test design document added. Unit tests: 27 passing in CI.
Blocked: browser tests cannot run from Codespaces. A connection to the site from there times out (curl to evalytics.in fails, curl to example.com works). Asked the owner about allow-listing or a staging copy. Browser tests will run from a local machine in the meantime.
Next: run the public pages smoke suite from a machine that can reach the site (S0021), finish the open public pages checks, plan the Sprint 0 review.
Hours remaining: 30
Notes: add "network access from cloud machines" to the risk register.
