---
id: EVA-DOC-001
title: Evalytics Master Test Plan
version: 0.3.0-draft
status: Draft
owner: MadhaviJ
created: 2026-11-14
updated: 2026-11-27
supersedes: 0.2.0-draft
sut: https://evalytics.in (v1.1.0 observed)
methodology: Agile (Scrum-style, 2-week sprints)
---

# Evalytics Master Test Plan

## 1. Purpose and Goals

**Purpose:** Verify the quality of Evalytics, an AI-powered online exam portal for coaching academies, across functional, non-functional and security dimensions (AI-functionality testing is deferred, ADR-0001), and set up AI agents that keep testing the application as it changes.

**Goals**

| # | Goal | Success measure |
|---|------|-----------------|
| G1 | **Functional testing** of every module | 100% of P0 and at least 90% of P1 stories executed; defects triaged |
| G2 | **Unit testing (if possible)** | Unit tests exist for this repo's own code. Unit tests for the app itself only if the owner shares source or components (see 5.4) |
| G3 | **Load testing** | Documented response, error and correctness figures at expected concurrent exam load, run only where the owner has approved |
| G4 | **Stress testing** (deferred, ADR-0002) | Documented breaking point, failure behaviour and recovery. Runs only on a staging environment, so it is deferred while none exists |
| G5 | **Security testing** | Authorized, non-destructive checks of authentication, authorization, session, lockout and tenant isolation completed; findings reported privately |
| G6 | **Testing the underlying AI functionality** (deferred, ADR-0001) | Out of scope for now. M05, M06, M07, M13 and M14 are listed as untested in the final report; the strategy in 5.3 is kept for later |
| G7 | **Accessibility testing** | WCAG 2.2 AA findings for key student and teacher flows, automated and manual |
| G8 | **API testing** | Contract, negative and authorization tests on the discovered endpoints |
| G9 | **AI agents that test existing and new features** | Agents run charters and exploration, file reproducible reports, detect new or changed features, and are benchmarked against the scripted suite |

**Non-goals:** AI-feature testing for now (ADR-0001), stress testing against production while no staging environment exists (ADR-0002), denial-of-service testing aimed at harming the service, load or stress testing production without written owner approval, testing third-party services (email, payment gateway) beyond integration touchpoints, destructive tests against other tenants.

## 2. Authorization and Ethical Guardrails

You've stated you're authorized. Record that in the repo anyway, because it protects you.

- [ ] Store a written authorization note (email or message from the owner) in `docs/governance/AUTHORIZATION.md`, with scope, dates, and permitted test types, especially **security, load and stress**.
- [ ] Test only in **your own** academy/tenant. The landing page shows testimonials from real students at "Pinnacle" academies, so real users and real data exist in production. Never touch other tenants beyond *deliberate, owner-approved* isolation probes using accounts you control on both sides.
- [ ] Use dedicated test mailboxes only. The platform sends real emails and calendar invites.
- [ ] AI features are out of scope for now (ADR-0001): do not use upload, AI generation, Genie or translation. Throttle automation so tests and agents don't degrade the service for real users.
- [ ] **Load and stress tests need their own written approval:** maximum virtual users, request rates, start and end time, and a named contact who can stop the test. Run on staging. If only production exists, run in a window agreed with the owner when no real exams are scheduled.
- [ ] Load-test students live only in dedicated academies (`eva-load-<n>`), use synthetic names (`loadtest-sNNN`), and are listed in a CSV so the owner can delete them afterwards. Accounts are created slowly, in small batches.
- [ ] Bulk-created students use a mail domain I control with a catch-all inbox, or the owner switches off emails for the load-test academies.
- [ ] **Capacity rule from the owner:** automation must not impact server capacity. All automation follows `docs/governance/CAPACITY-RULES.md` (one browser at a time, throttled requests, gradual load steps, abort rules). The owner's approval is currently verbal; get it confirmed in writing before any load test.
- [ ] Agent guardrails: allow-list of domains, rate limits, a kill switch, and no autonomous exploitation. Agents observe and report. Agents never use upload, AI generation, Genie or translation (ADR-0001).
- [ ] Ask whether a staging environment exists. If yes, run all load, stress and security work there.

## 3. System Under Test: Initial Reconnaissance

Based on the public pages (home, pricing, login). Authenticated areas are **not yet explored**; Sprint 0 covers that.

### 3.1 Architecture signals
- Multi-tenant SaaS with per-academy subdomains (`<academy>.evalytics.in`) and a central login that resolves the academy from the email
- Roles: Academy Owner, Teacher, Student (owner approval required for new teachers/students)
- Public routes seen: `/`, `/pricing`, `/login`, `/register`, `/forgot-password`, `/create-academy`
- Student join via **invite code**; students can belong to multiple academies with one login
- Plans: Solo, Academy, Pro, Enterprise; monthly or academic-year (10 months) billing; 15-day trial
- Version string in footer: `v1.1.0` (used to tag test runs and to detect new releases)

### 3.2 Feature inventory (test-object candidates)

`docs/modules.yaml` is the source of truth for module scope and priority; this table is a summary. M05, M06, M07, M13 and M14 are out of scope by choice (ADR-0001).

| ID | Module | Key behaviours claimed |
|----|--------|------------------------|
| M01 | Academy creation and onboarding | Subdomain selection, plan/seat calculator, trial start |
| M02 | Authentication and session | Email login, 30-day "keep me logged in", forgot password, lockout after failed attempts, session token bound to device |
| M03 | Roles and approvals | Owner approves teachers/students, separate teacher login, role isolation |
| M04 | Enrollment and batches | Request, approve/reject, unenroll with mandatory reason (shown to student), invite code |
| M05 | Question bank (out of scope, ADR-0001) | PDF/DOCX upload, AI MCQ extraction (tables, diagrams, formulas), difficulty tags (E/M/H), edit |
| M06 | AI explanations (out of scope, ADR-0001) | Auto step-by-step solution per question |
| M07 | Equation converter (out of scope, ADR-0001) | Unicode / image / OMML → LaTeX with preview |
| M08 | Test paper builder | Manual pick, random by chapter/difficulty mix, duration, marking scheme, reuse |
| M09 | Exam scheduling | Date/time windows, email + calendar invite, 10-min warning, auto-submit |
| M10 | Exam taking (student) | Timed exam, auto-save, language switch, resume after disconnect |
| M11 | Results and analytics | Instant score, correct answers, averages, pass rate, top performers, history, leaderboard |
| M12 | Re-attempt requests | Student requests, teacher handles |
| M13 | Genie AI assistant (out of scope, ADR-0001) | Natural-language queries over tenant data |
| M14 | Multilingual (out of scope, ADR-0001) | EN / HI / MR / KN AI-translated exams |
| M15 | Activity log and error tracking | Audit trail per academy |
| M16 | Bug report form | Screenshot upload |
| M17 | Pricing and billing | Calculator, prorating, add-ons, annual vs monthly |
| M18 | Multi-tenancy isolation | Cross-academy data separation |

### 3.3 Early observations (hypotheses to verify, not confirmed defects)
1. **Pricing page plan matrix:** "White-label branding" and "API access" appear as included under *Academy* but marked "Soon" under *Pro*. Possible content inconsistency.
2. **Seat calculator:** The slider/range labels render as concatenated numbers (`420`, `101000`), which looks like min/max values merged without separators. Possible UI defect.
3. **Plan description:** Academy and Pro both say "from 4 teachers · 10 students", so the lower bound doesn't differentiate them. Possible copy issue.
4. **Seat definitions:** Solo is capped at 50 students, but what happens when the 51st student requests enrollment? Needs a boundary test.
5. **Marketing claims to verify:** "under 10 seconds" extraction, "instant" results, "tamper-proof sessions", "protected against repeated login attempts", "academy data fully isolated", and "zero third-party trackers". Not verified in this version: the "under 10 seconds" extraction claim (M05 deferred, ADR-0001).
6. **Genie accuracy risk:** An LLM answering from live data is a hallucination and data-leak risk (cross-tenant, cross-student). Genie testing is deferred (ADR-0001), so this risk stays untested.
7. **Testimonial list** appears duplicated on the page (likely a carousel loop); check for accessibility and rendering issues.

## 4. Scope

### 4.1 In scope
Functional (all modules above except the deferred AI modules in 4.2), UI/UX, unit tests for this repo's code (and for the app if source is shared), API/network layer, authentication/authorization, tenant isolation, responsive/mobile, cross-browser, accessibility, load and stress testing (with approval), email notification content, data integrity of scoring and analytics, and the AI-agent testing layer.

### 4.2 Out of scope (initially)
AI features M05, M06, M07, M13 and M14, and anything that depends on AI quota or AI translation (deferred by choice, ADR-0001), and stress testing while no staging environment exists (ADR-0002). Payment gateway internals, email-provider deliverability, infrastructure-level attacks, and WhatsApp alerts (marked "Coming soon"). Re-assess after Sprint 0.

## 5. Test Approach

### 5.1 Risk-based prioritization

| Risk area | Impact | Likelihood | Priority | Rationale |
|-----------|--------|------------|----------|-----------|
| Tenant data isolation | Critical | Medium | **P0** | Core trust claim; students' data |
| Exam timing, auto-submit, auto-save, scoring correctness | Critical | Medium | **P0** | Core product value; disputes |
| Authentication, lockout, session binding | High | Medium | **P0** | Security claims |
| Behaviour under concurrent exam load | High | Medium | **P1** | A whole class submits at the same deadline |
| Genie data access and grounding | High | High | **P1** | LLM hallucination/leak (deferred, ADR-0001) |
| AI extraction accuracy | High | High | **P1** | Garbage in leads to wrong answer keys (deferred, ADR-0001) |
| Role/approval workflows | High | Medium | **P1** | Privilege boundaries |
| Accessibility of exam flow | Medium | Medium | **P2** | Timer, keyboard use, math content |
| Scheduling, invites, notifications | Medium | Medium | **P2** | Time zones, windows |
| Multilingual rendering and translation | Medium | High | **P2** | Devanagari and Kannada fonts, LaTeX in translation (deferred, ADR-0001) |
| Pricing/billing UI | Medium | Low | **P3** | Mostly display unless billing is live |

### 5.2 Test levels and types

| Goal | Level | Technique | Tooling (proposed) |
|------|-------|-----------|--------------------|
| G1 | Exploratory | Session-based test management (SBTM) charters, 60-90 min | Notes in `exploratory/`, screen recordings |
| G1 | UI functional | Page-object model, data-driven; Chromium, Firefox, WebKit, mobile emulation | Playwright (TypeScript) |
| G2 | Unit | Tests for repo utilities, scorers, agent code; app unit tests only if source is shared | Vitest / pytest |
| G3 | Load | Scripted concurrent exam-taking flow at expected class sizes | k6 |
| G4 | Stress (deferred, ADR-0002) | Step and spike ramps to find the breaking point; recovery checks. Needs a staging environment | k6 |
| G5 | Security (authorized, non-destructive) | OWASP ASVS L1 and Top 10 checklist, IDOR/tenant probes | Burp CE / ZAP in passive mode, manual |
| G6 | AI quality (deferred, ADR-0001) | Golden datasets, rubric/LLM-as-judge, metamorphic tests | Python eval harness |
| G7 | Accessibility | WCAG 2.2 AA automated + manual keyboard/screen-reader | axe-core, NVDA/VoiceOver |
| G8 | API | Contract and negative tests after endpoint discovery | Playwright APIRequest or pytest + httpx, schemathesis if OpenAPI exists |
| G9 | AI-agent testing | Charter-driven and exploratory autonomous agents | See section 6 |

### 5.3 AI feature test strategy (M05, M06, M07, M13, M14)

> **Deferred (ADR-0001).** This section is kept as the strategy for when AI testing is re-enabled. Do not run these tests against the trial quota.

LLM features are non-deterministic, so exact-match assertions don't work.
- **Golden corpus:** 15-20 PDFs (clean, scanned, two-column, table-heavy, diagram-heavy, chemistry structures, Hindi/Marathi) with a hand-built ground-truth JSON of questions, options, and answer keys.
- **Metrics:** question recall and precision, option accuracy, answer-key accuracy, diagram attachment accuracy, time-to-extract (vs the "10 seconds" claim).
- **Explanations:** rubric scoring (correctness, step validity, consistent with the answer key). Flag cases where the explanation contradicts the key.
- **Genie:** curated question set with known answers computed independently via SQL or UI export. Check numeric accuracy, refusal behaviour for out-of-scope or cross-tenant questions, and prompt-injection resistance (e.g., a student name or question text containing instructions).
- **Translation:** back-translation and bilingual reviewer sampling; verify numbers, units, chemical formulas, and LaTeX survive translation.
- **Budget:** trial quotas are tiny (5 per feature), so plan a paid add-on or owner-granted quota. Otherwise the AI evaluation can't reach a useful sample size.

### 5.4 Unit testing strategy (G2)
Unit tests need access to the code under test, and the Evalytics source is not available. The plan therefore treats this goal in three tiers:
1. **Always:** unit tests for this repo's own code, including test helpers, data generators, AI scorers, report generators and agent guardrail logic. Target: tests run in CI on every pull request.
2. **If the owner shares components or logic** (for example scoring, marking schemes, timer or auto-submit calculations): write unit tests for those directly, and trace them to M08 to M11.
3. **Otherwise:** use narrow, single-endpoint API checks (see G8) as the closest black-box substitute, and record in an ADR that app-level unit testing was not possible.

### 5.5 Load and stress testing strategy (G3, G4)
**Preconditions:** written owner approval covering limits, time window, environment and a stop contact (section 2). Staging preferred. Student accounts are created in dedicated load-test academies, in small batches, with emails handled first (section 2), and the owner deletes them afterwards. There is no staging environment at present (ADR-0002): load tests run on dedicated QA academies in production, within `docs/governance/CAPACITY-RULES.md`, and stress testing is not run. Load is generated at protocol level with k6, not with 500 real browsers, and the owner allow-lists the load tool's IP address if bot protection would block it.

**Scenarios**
- **Class exam load:** N students log in, open the exam, answer with auto-save, and submit. Increase N gradually: 10, 25, 50, 100, 150, 200, 300, 400, 500, moving up only if the previous step was clean. The target ceiling is 500 students. The maximum actually allowed is the one the owner confirms in writing, and the ladder, gates and abort rules are in `docs/governance/CAPACITY-RULES.md`.
- **Deadline surge:** many students submit within the same minute as the auto-submit deadline.
- **Teacher analytics load:** results and leaderboard views while an exam is being submitted.
- **Stress (deferred while no staging environment exists, ADR-0002):** step ramp beyond the expected load until errors or latency cross a threshold, plus a short spike test, then verify recovery.

**Exclusions:** AI endpoints (extraction, explanations, Genie, translation) are not load tested. They cost money and are rate-limited, so use single calls and small batches.

**Measures:** p50, p95 and p99 response time, error rate, auto-save success, submit success, **score correctness under load** (no lost or duplicated answers), time to recover after the peak.

**Abort rules:** stop at once if the error rate or latency crosses the agreed ceiling, if the owner asks, or if real users report problems.

### 5.6 Accessibility testing strategy (G7)
- Automated axe-core scans in the UI suite on every key page.
- Manual keyboard-only pass of login, enrollment, exam taking and results.
- Screen-reader pass (NVDA on Windows, VoiceOver on Mac/iOS) of the exam flow.
- Exam-specific checks: timer and 10-minute warning announced to assistive technology, focus order when switching language, contrast, reflow at 400% zoom, touch target size on phones, and whether rendered equations are readable by screen readers.
- Language attributes and font rendering for Hindi, Marathi and Kannada content.

### 5.7 API testing strategy (G8)
- Discover endpoints from browser network captures (HAR) on your own tenant.
- Contract checks: status codes, schemas, headers.
- Negative checks: bad input, missing fields, oversized payloads, wrong content types.
- Authorization checks (shared with G5): student calling teacher endpoints, one tenant calling another's identifiers, expired or tampered tokens.
- Behaviour checks: idempotent auto-save and submit, server-side time enforcement for exam windows, lockout and rate-limit responses.

## 6. AI-Agent Testing Layer (G9)

### 6.1 Philosophy
Agents don't replace the deterministic suite. They add **breadth, exploration, change detection and natural-language oracles**. The scripted suite is the benchmark and safety net.

### 6.2 Progression

| Stage | Description | Exit criterion |
|-------|-------------|----------------|
| A1 | **Agent-assisted authoring:** LLM drafts test cases and page objects from the feature inventory; human reviews | 50+ reviewed cases in Git |
| A2 | **Agent-executed scripted charters:** Agent follows a written charter in a real browser (Playwright MCP / browser-use style), reports pass/fail with evidence | ≥80% agreement with scripted tests on the same scenarios |
| A3 | **Exploratory agents:** Persona-based agents (new teacher, anxious student on a slow phone, adversarial student, Marathi-speaking user) explore freely within guardrails | Agents find ≥1 defect the scripted suite missed |
| A4 | **Oracle agents:** Agents verify deterministic outputs (scoring, results, analytics) against hand-calculated answer keys. AI-feature oracles (Genie, extraction) are deferred (ADR-0001) | Metrics dashboard produced per run |
| A5 | **Orchestrated multi-agent run in CI with change detection:** Planner, executor, triager, and reporter agents. A change-detection agent notices a new version string, new pages or menu items, or changed pages, drafts charters for them, and runs a first exploration | Nightly run publishes a report PR; a new or changed feature gets a drafted charter and a first report within one run |

### 6.3 Handling new features
- Track the footer version (`v1.1.0` and later) and a sitemap snapshot, and compare them each run.
- When something changes, the agent drafts a charter and test-case stubs in a pull request for human review. A human decides what becomes a permanent test.
- New features first get exploratory agent coverage, then scripted tests once understood.

### 6.4 Agent design requirements
- Structured outputs (JSON schema) for steps, evidence (screenshots/HAR/trace), verdict, and confidence
- Deterministic replay: store prompts, model version, seed/temperature, and traces for every run
- Guardrails: domain allow-list, action allow-list (no account deletion, no payment, no upload, AI generation, Genie or translation), spending and rate caps (see `docs/governance/CAPACITY-RULES.md`), kill switch
- Triage step to de-duplicate and rate-limit bug filing (LLM false positives are the main risk)
- Metrics: defects found, false-positive rate, cost per run, run-to-run variance, coverage vs scripted suite

## 7. Test Environment and Data

| Item | Plan |
|------|------|
| Environments | Production (own tenant, low-volume). No staging environment exists at present (ADR-0002); all testing runs against production QA academies under `docs/governance/CAPACITY-RULES.md`. Request staging for stress and security work |
| Tenants | `eva-qa-<n>.evalytics.in` (own trial academy; ask owner for upgraded limits); load-test academies `eva-load-<n>.evalytics.in`, created only after load and stress approval is confirmed |
| Accounts | 1 owner, 2 teachers (one pending), 6+ students across 2 tenants for isolation tests; scripted student accounts (`loadtest-sNNN`, up to 500) for load tests, created in small batches and listed in a CSV |
| Email | Plus-addressed Gmail or a disposable test inbox with API (e.g., Mailosaur / MailHog equivalent); a catch-all domain for bulk accounts, or emails switched off by the owner for load-test academies |
| Data | Synthetic only. A hand-made 20-question set with a known answer key (golden PDFs deferred, ADR-0001). No real student data |
| Devices/browsers | Chrome, Firefox, Safari/WebKit, Edge; Android Chrome and iOS Safari (real or emulated) |
| Observability | Playwright traces, HAR, video on failure; Git-stored run artifacts (summaries, not heavy binaries; use Git LFS or release assets for large files) |
| Time handling | Scheduling tests need clock awareness (IST vs browser time zone, DST for non-IST testers) |

## 8. Git-Based "JIRA" Model

Everything lives in one repo (`evalytics-ai-tester`). Work items are files, so history, review, and traceability come for free. Sprints run on the **EvalyticsQA** GitHub Project (Sprint iteration field, Estimates field, Status board). Issues on the board mirror the files in `backlog/`.

### 8.1 Proposed repository layout

```
evalytics-ai-tester/
├── README.md
├── docs/
│   ├── test-plan/TEST-PLAN.md            # this document
│   ├── test-plan/ESTIMATES.md            # (generated from backlog)
│   ├── governance/AUTHORIZATION.md
│   ├── governance/CAPACITY-RULES.md      # limits that keep automation light on the server
│   ├── risk-register.md
│   ├── modules.yaml                      # module list, scope, priority (source of truth)
│   └── adr/                              # architecture decision records
├── backlog/
│   ├── epics/EVA-E01-*.md
│   ├── stories/EVA-S0001-*.md
│   ├── tasks/EVA-T0001-*.md
│   ├── bugs/EVA-B0001-*.md               # defects found in the SUT
│   └── spikes/EVA-SP0001-*.md
├── sprints/
│   ├── sprint-00/{plan.md,review.md,retro.md,burndown.csv}
│   └── ...
├── test-cases/                           # manual/automated case specs (YAML/MD)
├── charters/                             # exploratory + agent charters
├── automation/
│   ├── ui/                               # Playwright
│   ├── api/
│   ├── performance/                      # load and stress scripts
│   ├── ai-eval/                          # golden datasets, scorers
│   └── agents/                           # agent harness, prompts, guardrails
├── scripts/                              # helper scripts (coverage_check.py)
├── reports/                              # run summaries, dashboards
└── .github/
    ├── ISSUE_TEMPLATE/, PULL_REQUEST_TEMPLATE.md
    └── workflows/                        # CI, nightly agent run
```

### 8.2 Object definitions (Jira analogues)

| Jira concept | Git artifact | ID format | Notes |
|--------------|--------------|-----------|-------|
| Epic | `backlog/epics/*.md` | `EVA-E##` | Maps to a test area (Section 9) |
| Story | `backlog/stories/*.md` | `EVA-S####` | User-value statement + acceptance criteria |
| Task / Sub-task | `backlog/tasks/*.md` | `EVA-T####` | Atomic work, ≤8h |
| Bug | `backlog/bugs/*.md` | `EVA-B####` | Defects in the SUT |
| Spike | `backlog/spikes/*.md` | `EVA-SP####` | Time-boxed investigation |
| Test case | `test-cases/*.yaml` | `EVA-TC####` | Linked to story and requirement |
| Test run/cycle | `reports/runs/<date>/` | `EVA-TR####` | Auto-generated |
| Sprint | `sprints/sprint-NN/` | `S##` | Plan, review, retro |
| Board | GitHub Project "EvalyticsQA" | n/a | Columns: Backlog, Ready, In Progress, In Review, Done, Won't do (skipped items, with the reason) |
| Workflow transition | PR merge + `status` field | n/a | Status changes via PR |

### 8.3 Sample story (template)

```markdown
---
id: EVA-S0100
type: story
epic: EVA-E07
title: Student exam auto-submits at deadline
status: Backlog          # Backlog | Ready | In Progress | In Review | Done
priority: P0
estimate_hours: 5        # most likely
estimate_range: [3, 9]   # optimistic, pessimistic
sprint: null
labels: [exam, timing, automation]
covers: [M09, M10]
links: { blocks: [], depends_on: [EVA-T0004], tests: [EVA-TC0031] }
---
## Description
As a student, when the exam window closes my answers are submitted automatically.

## Acceptance Criteria
- [ ] Given an exam ending at T, when T passes, then the attempt is submitted with saved answers
- [ ] 10-minute warning shown at T-10m
- [ ] Late submit attempts are rejected with a clear message

## Test Notes
Use a short window (e.g., 12 min) in the QA tenant; verify server-side time, not client clock.
```

### 8.4 Git workflow and Definition of Done
- **Branching:** trunk-based with short-lived branches: `feat/EVA-S0100-autosubmit-test`, `fix/…`, `docs/…`
- **Commits:** Conventional Commits, referencing IDs: `test(exam): add auto-submit deadline spec [EVA-S0100]`
- **PRs:** required template (linked item, evidence, flake check); CI must pass; self-review checklist as a solo practitioner
- **Tags/releases:** `sprint-NN` tags at sprint end; `sut-v1.1.0-baseline` for the first baseline run
- **Definition of Ready:** acceptance criteria written, estimate present, data/accounts available
- **Definition of Done:** code/test reviewed and merged, runs green 3 consecutive times, traceability links updated, docs updated, artifacts in `reports/`

## 9. Work Breakdown and Estimates (Man-Hours)

**Method:** Bottom-up three-point estimate per epic (expected = (O + 4M + P) / 6), then a single sanity check against capacity. The numbers below are **planning estimates before authenticated reconnaissance**. They will be re-baselined after Sprint 0 (task EVA-T0002), and the plan expects roughly ±25% accuracy at this stage.

**Assumptions:** one primary QA engineer (you), AI coding assistants available, access to an upgraded trial or staging tenant, no blocking environment issues, owner approval for load testing within his condition that automation must not impact server capacity (verbal, written confirmation pending), no staging environment (so no stress testing), and **no access to the app's source code** (unit testing covers repo code only, see 5.4). AI features are out of scope (ADR-0001).

| Epic | Description | Goal | Hours |
|------|-------------|------|------:|
| EVA-E01 | Project setup: repo, board, templates, CI skeleton, conventions | all | 10 |
| EVA-E02 | Discovery and recon (authenticated walkthrough, endpoint mapping, sitemap) | all | 16 |
| EVA-E03 | Test design: cases, charters, traceability matrix, risk register | all | 32 |
| EVA-E04 | Environment and test data: tenants, accounts, mailbox, hand-made question set, load-test student seeding (golden PDFs deferred) | all | 14 |
| EVA-E05 | Exploratory and manual functional baseline, defect reporting | G1 | 36 |
| EVA-E06 | Automation framework: Playwright, fixtures, page objects, reporters, CI | G1 | 36 |
| EVA-E07 | UI functional automation, including cross-browser and responsive checks | G1 | 62 |
| EVA-E08 | Unit testing: repo code, plus app components if source is shared | G2 | 14 |
| EVA-E09 | API testing | G8 | 24 |
| EVA-E10 | Security testing (authorized, non-destructive) | G5 | 28 |
| EVA-E11 | AI functionality testing, including translation and multilingual (deferred, ADR-0001) | G6 | 0 |
| EVA-E12 | Accessibility testing | G7 | 14 |
| EVA-E13 | Load testing | G3 | 20 |
| EVA-E14 | Stress testing (deferred while no staging environment exists, ADR-0002) | G4 | 0 |
| EVA-E15 | **AI-agent testing layer** (A1-A5, including change detection) | G9 | 72 |
| EVA-E16 | Reporting and dashboards | all | 14 |
| EVA-E17 | Agile ceremonies and project management (~2.5h/week) | all | 24 |
| | **Subtotal** | | **416** |
| | Contingency (15%) | | 62 |
| | **Total** | | **≈ 478 h** |

Compared with version 0.1.0 (518 h), the total rose by about 36 hours. Unit, load and stress testing were added, accessibility became its own epic, and the agent layer grew to cover change detection. The showcase write-up was removed. Version 0.3.0 defers AI functionality testing (E11, 52 h, ADR-0001) and stress testing (E14, 14 h, ADR-0002, no staging environment), so the total drops by about 76 h to about 478 h.

### 9.1 Duration by capacity

| Weekly productive hours | Calendar duration | 2-week sprints |
|------------------------:|------------------:|---------------:|
| 15 h (side project) | ~32 weeks | ~16 |
| 20 h | ~24 weeks | ~12 |
| 30 h | ~16 weeks | ~8 |
| 40 h (full-time) | ~12 weeks | ~6 |
| Fast-track (about 151 h) at 40 h | ~4 weeks | see 9.4 |
| Fast-track (about 151 h) at 20 h | ~8 weeks | see 9.4 |

### 9.2 Effort distribution
~12% planning and design, ~28% framework and functional automation, ~14% security, API and accessibility testing (AI-feature testing deferred, ADR-0001), ~4% load testing (stress deferred), ~13% agents (post-baseline), and the remainder in exploratory, reporting and project management. Percentages are approximate and will be re-baselined after Sprint 0. Agents are deliberately built **after** the scripted baseline exists, so you have a ground truth to measure them against.

### 9.3 Estimate-reduction levers
- AI-assisted test authoring (can shave 15-25% off E03, E07)
- Reducing accessibility depth to the exam flow only (E12)
- Reusing community Playwright MCP / agent frameworks instead of building a harness from scratch (E15)
- Reducing load and stress to a single scenario each if the owner limits approval (E13, E14)

### 9.4 Fast-track variant (ADR-0003)

Target: about 151 h, about 19 working days at 8 h/day, estimate accuracy about ±30%. The ten sprints are compressed into four bursts. Hours are a proposal and will be re-baselined after Sprint 0.

| Epic | Fast-track hours | Note |
|------|-----------------:|------|
| EVA-E01 | 3 | Skip fancy templates, minimal CI |
| EVA-E02 | 6 | One careful walkthrough, taking notes |
| EVA-E03 | 8 | P0 and P1 areas only, AI-drafted cases |
| EVA-E04 | 9 | 20 hand-made questions, seeding up to 500 load-test students (owner bulk import preferred), catch-all mailbox |
| EVA-E05 | 16 | Four 90-minute sessions on the riskiest areas |
| EVA-E06 | 10 | Use the Playwright recorder, light page objects |
| EVA-E07 | 20 | P0 flows only, plus a three-browser run |
| EVA-E08 | 3 | Unit tests for repo scripts (for example the coverage check) |
| EVA-E09 | 6 | Inspect network calls, test a handful |
| EVA-E10 | 10 | Isolation, lockout, session only |
| EVA-E11 | 0 | Deferred (ADR-0001) |
| EVA-E12 | 5 | axe on key pages, keyboard pass of the exam flow |
| EVA-E13 | 12 | k6 exam flow, ladder up to a target of 500 students, only as far as the owner approves |
| EVA-E14 | 0 | Deferred: no staging environment (ADR-0002) |
| EVA-E15 | 14 | A1-A2 plus one exploratory persona; no nightly CI run |
| EVA-E16 | 6 | Short report and README |
| EVA-E17 | 3 | A 15-minute weekly check |
| | **131** | Subtotal |
| | 20 | Contingency (15%) |
| | **≈ 151 h** | Total |

| Burst | Covers | Working days |
|-------|--------|--------------|
| 1 | S0 and the start of S1 | 1-5 |
| 2 | S1-S3 | 6-10 |
| 3 | S4-S7, trimmed | 11-15 |
| 4 | S8-S9 | 16-19 |

Not negotiable when rushing: written authorization, testing only the own tenant, throttled runs, security findings kept private, and agents built last so the scripted tests act as the answer key.

## 10. Proposed Sprint Roadmap (30 h/week example, 2-week sprints)

| Sprint | Theme | Key outputs |
|--------|-------|-------------|
| **S0** | Foundations and recon | Repo, board, authorization note, tenants, sitemap, endpoint map, refined estimates, risk register v1 |
| **S1** | Test design and manual functional baseline | Traceability matrix, 60+ cases, first exploratory sessions, first bug reports |
| **S2** | Automation framework and P0 smoke | CI green, unit-test setup, auth + enrollment + academy creation smoke suite |
| **S3** | P0/P1 functional automation | Question bank, paper builder, scheduling, exam taking, results |
| **S4** | Security and API | Isolation and authz suite, API checks, findings report (private) |
| **S5** | AI functionality evaluation (deferred, ADR-0001) | Skipped for now; revisit if the owner grants quota |
| **S6** | Cross-browser, accessibility (i18n deferred with M14) | Compatibility matrix, WCAG findings |
| **S7** | Load testing (stress deferred, ADR-0002) | Approved load scenarios within the capacity rules, load report |
| **S8** | Agents A1-A3 | Agent harness, charter execution, persona exploration, comparison to scripted suite |
| **S9** | Agents A4-A5 and hardening | Oracle agents, change detection, nightly CI run, flake reduction, final report |

Re-plan every sprint using actual velocity (hours completed vs planned). At 20 h/week the same plan runs to about 12 sprints, so later themes shift out accordingly. Fast-track (section 9.4, ADR-0003): sprints are compressed into four bursts. Stress testing in S7 is deferred until a staging environment exists (ADR-0002).

## 11. Entry and Exit Criteria

**Entry (per phase):** environment reachable, test accounts provisioned, authorization on file, stories Ready. For load and stress phases, also: written approval with limits and a named stop contact.

**Exit (overall):**
- 100% of P0 and ≥90% of P1 stories executed, with results traceable to requirements
- No open Critical/High defects without an agreed disposition
- Automated regression suite stable (<5% flaky across 10 runs)
- Unit tests for repo code running in CI
- Load report delivered with the approved scenarios, limits and findings (stress testing deferred, ADR-0002)
- AI features deferred (ADR-0001): the final report lists M05, M06, M07, M13 and M14 as not tested, not as passed
- Accessibility findings documented against WCAG 2.2 AA for the key flows
- Agent benchmark report: coverage, defects, false-positive rate, cost, and new-feature detection results
- All artifacts committed, sprints closed with review and retro

## 12. Defect Management

- Severity: S1 Critical (data leak, wrong score, exam lost), S2 High, S3 Medium, S4 Low
- Required fields: ID, title, environment/version, steps, expected/actual, evidence, severity/priority, linked test case
- Security findings go to a **private** `security/` folder or private repo, with coordinated disclosure to the owner before anything is published. Redact tenant specifics in any public write-up.

## 13. Metrics and Reporting

Requirement/risk coverage, pass rate by run, defect density and escape analysis, automation ROI (hours saved vs invested), flake rate, load and stress figures (p95 latency, error rate, breaking point), accessibility issues by severity, AI metrics (deferred), mean time to detect for agents vs scripts, agent false-positive rate, new-feature detection time, cost per agent run, sprint velocity and burndown.

## 14. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Testing against production affects real users | Med | High | Own tenant, throttling, staging request, off-peak runs |
| Load or stress test degrades the live service | Med | High | Written approval of the maximum, gradual steps with a gate between them, abort rules, owner watching server load for steps above 100, named stop contact |
| Bulk student creation floods real email | Med | Med | Catch-all test domain, or owner switches off emails for load-test academies |
| Everyday automation (UI suite, API checks, agents) uses server capacity | Med | High | `docs/governance/CAPACITY-RULES.md`: one browser at a time, throttled requests, step and time caps; the owner can stop any run |
| No staging environment exists | High | Med | Stress testing deferred; load tests limited to small steps on dedicated QA academies; ask the owner whether a staging instance can be created |
| Owner authorization is verbal only | Med | High | Get written confirmation of the load limits before any load test; record the verbal approval in `AUTHORIZATION.md` |
| No source code, so unit testing of the app is impossible | High | Low | Three-tier approach in 5.4; record outcome in an ADR |
| Owner limits or declines load and stress testing | Med | Med | Reduce to single scenarios (see 9.3); document the gap |
| AI features are not tested (deferred, ADR-0001), so extraction, explanation, Genie and translation risks stay open | High | Med | List M05, M06, M07, M13, M14 as untested in the final report; revisit if the owner grants quota |
| Authorization scope ambiguity (security testing) | Med | High | Written scope; non-destructive only |
| Email-dependent flows are hard to automate | Med | Med | Mailbox API, plus-addressing |
| Time-based flows are slow/flaky | High | Med | Short exam windows in QA tenant; server-time assertions |
| LLM agent false positives and nondeterminism | High | Med | Structured verdicts, evidence, triage agent, replay logs |
| Agents miss or misread new features | Med | Med | Version and sitemap diffing; human review of drafted charters |
| Bot protection / rate limiting blocks automation | Med | Med | Coordinate allow-listing with owner |
| SUT changes during project (v1.1.0 to later) | High | Med | Version-tag every run; keep tests resilient (roles/test-ids) |
| Scope creep | Med | Med | Sprint-gated backlog, change log in ADRs |

## 15. Open Questions (to resolve in Sprint 0)

1. There is currently no staging environment. Can a staging instance be created for stress and security work, and can the seat limit be raised to 500 students for load testing (or can he bulk-create the students)?
2. What security test types are explicitly permitted (brute-force lockout, IDOR probes, passive scanning)?
3. **The owner has verbally approved testing that does not impact server capacity. Can he confirm in writing the load limits (target up to 500 students, gradually; time window; quiet hours)?** Stress testing needs a staging environment (ADR-0002).
4. **Can the owner share any source code or components (for example scoring or timer logic) for unit testing?**
5. Is billing/payment live in the trial flow, and should it be tested?
6. Is there API documentation (OpenAPI), given the "API access" plan feature?
7. Which LLM(s) and agent framework do you want to use for the agent layer (e.g., Claude via API with Playwright MCP)?
8. Is the repo public or private? This determines how findings are published.
9. Which weekly capacity should the plan be committed to (Section 9.1)?
10. Does the owner publish release notes or announce new features, so the change-detection agent has a second signal?
11. Is there a bulk student import or seed route, and can emails be switched off for the load-test academies?
12. Will the owner grant extra AI quota later, so AI-feature testing (ADR-0001) can be re-enabled?

## 16. Traceability Seeds

Each module (M01-M18) becomes at least one Epic-linked story set. Each story links to test cases (`EVA-TC####`) and each test case to automation file paths and agent charters, so the matrix `module → story → test case → automated/agent coverage` can be generated by script from front matter. `docs/modules.yaml` is the source of truth for module scope and priority, and `scripts/coverage_check.py` prints the gaps and the skipped modules.

## 17. Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-11-14 | MadhaviJ | Initial draft from public-page recon |
| 0.2.0 | 2026-11-15 | MadhaviJ | Goals rewritten to nine goals (added unit, load, stress, accessibility, API as explicit goals); strategies added for G2, G3/G4, G7, G8; agent layer extended with change detection; estimates re-baselined to about 554 h; sprint roadmap aligned with README; learning and showcase items removed |
| 0.3.0 | 2026-11-27 | MadhaviJ | AI-feature testing deferred (ADR-0001); load testing conditions and capacity rules recorded, stress testing deferred because there is no staging environment (ADR-0002); fast-track schedule added as 9.4 (ADR-0003); modules.yaml and coverage script added; estimates re-baselined to about 478 h |
