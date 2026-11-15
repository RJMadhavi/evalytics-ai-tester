---
id: EVA-DOC-001
title: Evalytics Master Test Plan
version: 0.1.0-draft
status: Draft
owner: <your-name>
created: 2026-11-14
sut: https://evalytics.in (v1.1.0 observed)
methodology: Agile (Scrum-style, 2-week sprints)
---

# Evalytics Master Test Plan

## 1. Purpose and Goals

**Purpose:** Verify the quality of Evalytics, an AI-powered online exam portal for coaching academies, and use the effort as a portfolio project demonstrating modern QA engineering.

**Primary goals**

| # | Goal | Success measure |
|---|------|-----------------|
| G1 | Establish a trustworthy functional, API, security, and non-functional baseline of the SUT | Risk-based coverage report with defects triaged |
| G2 | Build a maintainable automation framework | Green CI pipeline, <5% flaky tests |
| G3 | **Deploy AI agents that test the app** (end goal) | Agents execute defined charters, produce reproducible bug reports, and are benchmarked against scripted tests |
| G4 | Showcase engineering and process skill | Public repo with plan, estimates, traceability, dashboards, and a write-up |

**Non-goals:** Load/stress testing at production scale, destructive or denial-of-service testing, testing third-party services (email, payment gateway) beyond integration touchpoints.

## 2. Authorization and Ethical Guardrails

You've stated you're authorized. Record that in the repo anyway, because it protects you and gives the showcase credibility.

- [ ] Store a written authorization note (email or message from the owner) in `docs/governance/AUTHORIZATION.md`, with scope, dates, and permitted test types (especially security and performance).
- [ ] Test only in **your own** academy/tenant. The landing page shows live testimonials from real students at "Pinnacle" academies, so real users and real data exist in production. Never touch other tenants beyond *deliberate, owner-approved* isolation probes using accounts you control on both sides.
- [ ] Use dedicated test mailboxes only. The platform sends real emails and calendar invites.
- [ ] Respect trial AI quotas (5 uploads, 5 AI generations, 5 Genie questions) and throttle automation so agents don't degrade the service for real users.
- [ ] Agent guardrails: allow-list of domains, rate limits, a kill switch, and no autonomous exploitation. Agents observe and report.
- [ ] Ask whether a staging environment exists. If yes, run all heavy, security, and load work there.

## 3. System Under Test: Initial Reconnaissance

Based on the public pages (home, pricing, login). Authenticated areas are **not yet explored**; Sprint 0 covers that.

### 3.1 Architecture signals
- Multi-tenant SaaS with per-academy subdomains (`<academy>.evalytics.in`) and a central login that resolves the academy from the email
- Roles: Academy Owner, Teacher, Student (owner approval required for new teachers/students)
- Public routes seen: `/`, `/pricing`, `/login`, `/register`, `/forgot-password`, `/create-academy`
- Student join via **invite code**; students can belong to multiple academies with one login
- Plans: Solo, Academy, Pro, Enterprise; monthly or academic-year (10 months) billing; 15-day trial
- Version string in footer: `v1.1.0` (useful for tagging test runs)

### 3.2 Feature inventory (test-object candidates)

| ID | Module | Key behaviours claimed |
|----|--------|------------------------|
| M01 | Academy creation and onboarding | Subdomain selection, plan/seat calculator, trial start |
| M02 | Authentication and session | Email login, 30-day "keep me logged in", forgot password, lockout after failed attempts, session token bound to device |
| M03 | Roles and approvals | Owner approves teachers/students, separate teacher login, role isolation |
| M04 | Enrollment and batches | Request, approve/reject, unenroll with mandatory reason (shown to student), invite code |
| M05 | Question bank | PDF/DOCX upload, AI MCQ extraction (tables, diagrams, formulas), difficulty tags (E/M/H), edit |
| M06 | AI explanations | Auto step-by-step solution per question |
| M07 | Equation converter | Unicode / image / OMML → LaTeX with preview |
| M08 | Test paper builder | Manual pick, random by chapter/difficulty mix, duration, marking scheme, reuse |
| M09 | Exam scheduling | Date/time windows, email + calendar invite, 10-min warning, auto-submit |
| M10 | Exam taking (student) | Timed exam, auto-save, language switch, resume after disconnect |
| M11 | Results and analytics | Instant score, correct answers, averages, pass rate, top performers, history, leaderboard |
| M12 | Re-attempt requests | Student requests, teacher handles |
| M13 | Genie AI assistant | Natural-language queries over tenant data |
| M14 | Multilingual | EN / HI / MR / KN AI-translated exams |
| M15 | Activity log and error tracking | Audit trail per academy |
| M16 | Bug report form | Screenshot upload |
| M17 | Pricing and billing | Calculator, prorating, add-ons, annual vs monthly |
| M18 | Multi-tenancy isolation | Cross-academy data separation |

### 3.3 Early observations (hypotheses to verify, not confirmed defects)
1. **Pricing page plan matrix:** "White-label branding" and "API access" appear as included under *Academy* but marked "Soon" under *Pro*. Possible content inconsistency.
2. **Seat calculator:** The slider/range labels render as concatenated numbers (`420`, `101000`), which looks like min/max values merged without separators. Possible UI defect.
3. **Plan description:** Academy and Pro both say "from 4 teachers · 10 students", so the lower bound doesn't differentiate them. Possible copy issue.
4. **Seat definitions:** Solo is capped at 50 students, but what happens when the 51st student requests enrollment? Needs a boundary test.
5. **Marketing claims to verify:** "under 10 seconds" extraction, "instant" results, "tamper-proof sessions", "protected against repeated login attempts", "academy data fully isolated", and "zero third-party trackers".
6. **Genie accuracy risk:** An LLM answering from live data is a hallucination and data-leak risk (cross-tenant, cross-student).
7. **Testimonial list** appears duplicated on the page (likely a carousel loop); check for accessibility and rendering issues.

## 4. Scope

### 4.1 In scope
Functional (all modules above), UI/UX, API/network layer, authentication/authorization, tenant isolation, AI output quality, i18n/L10n, responsive/mobile, cross-browser, accessibility, light performance and resilience, email notification content, data integrity of scoring and analytics, and the AI-agent testing layer.

### 4.2 Out of scope (initially)
Payment gateway internals, email-provider deliverability, infrastructure/DDoS, and WhatsApp alerts (marked "Coming soon"). Re-assess after Sprint 0.

## 5. Test Approach

### 5.1 Risk-based prioritization

| Risk area | Impact | Likelihood | Priority | Rationale |
|-----------|--------|------------|----------|-----------|
| Tenant data isolation | Critical | Medium | **P0** | Core trust claim; students' data |
| Exam timing, auto-submit, auto-save, scoring correctness | Critical | Medium | **P0** | Core product value; disputes |
| Authentication, lockout, session binding | High | Medium | **P0** | Security claims |
| Genie data access and grounding | High | High | **P1** | LLM hallucination/leak |
| AI extraction accuracy | High | High | **P1** | Garbage in leads to wrong answer keys |
| Role/approval workflows | High | Medium | **P1** | Privilege boundaries |
| Scheduling, invites, notifications | Medium | Medium | **P2** | Time zones, windows |
| Multilingual rendering and translation | Medium | High | **P2** | Devanagari and Kannada fonts, LaTeX in translation |
| Pricing/billing UI | Medium | Low | **P3** | Mostly display unless billing is live |

### 5.2 Test levels and types

| Level | Technique | Tooling (proposed) |
|-------|-----------|--------------------|
| Exploratory | Session-based test management (SBTM) charters, 60-90 min | Notes in `exploratory/`, screen recordings |
| UI functional | Page-object model, data-driven | Playwright (TypeScript) |
| API | Contract and negative tests after endpoint discovery | Playwright APIRequest or pytest + httpx, schemathesis if OpenAPI exists |
| Security (authorized, non-destructive) | OWASP ASVS L1 and Top 10 checklist, IDOR/tenant probes | Burp CE / ZAP in passive mode, manual |
| AI quality | Golden datasets, rubric/LLM-as-judge, metamorphic tests | Python eval harness |
| i18n | Pseudo-localization, font rendering, translation fidelity review | Playwright + visual checks |
| Cross-browser/mobile | Chromium, Firefox, WebKit, mobile emulation, 2 real devices | Playwright projects |
| Accessibility | WCAG 2.2 AA automated + manual keyboard/screen-reader | axe-core, NVDA/VoiceOver |
| Performance (light) | Page-load budgets, small concurrency on exam-taking flow (on staging only) | Lighthouse, k6 (low VUs) |
| AI-agent testing | Charter-driven autonomous agents | See section 6 |

### 5.3 AI feature test strategy (M05, M06, M07, M13, M14)
LLM features are non-deterministic, so exact-match assertions don't work.
- **Golden corpus:** 15-20 PDFs (clean, scanned, two-column, table-heavy, diagram-heavy, chemistry structures, Hindi/Marathi) with a hand-built ground-truth JSON of questions, options, and answer keys.
- **Metrics:** question recall and precision, option accuracy, answer-key accuracy, diagram attachment accuracy, time-to-extract (vs the "10 seconds" claim).
- **Explanations:** rubric scoring (correctness, step validity, consistent with the answer key). Flag cases where the explanation contradicts the key.
- **Genie:** curated question set with known answers computed independently via SQL or UI export. Check numeric accuracy, refusal behaviour for out-of-scope or cross-tenant questions, and prompt-injection resistance (e.g., a student name or question text containing instructions).
- **Translation:** back-translation and bilingual reviewer sampling; verify numbers, units, chemical formulas, and LaTeX survive translation.
- **Budget:** trial quotas are tiny (5 per feature), so plan a paid add-on or owner-granted quota for the evaluation. Otherwise the AI evaluation can't reach a statistically useful sample size.

## 6. AI-Agent Testing Layer (End Goal)

### 6.1 Philosophy
Agents don't replace the deterministic suite. They add **breadth, exploration, and natural-language oracles**. The scripted suite is the benchmark and safety net.

### 6.2 Progression

| Stage | Description | Exit criterion |
|-------|-------------|----------------|
| A1 | **Agent-assisted authoring:** LLM drafts test cases and page objects from the feature inventory; human reviews | 50+ reviewed cases in Git |
| A2 | **Agent-executed scripted charters:** Agent follows a written charter in a real browser (Playwright MCP / browser-use style), reports pass/fail with evidence | ≥80% agreement with scripted tests on the same scenarios |
| A3 | **Exploratory agents:** Persona-based agents (new teacher, anxious student on a slow phone, adversarial student, Marathi-speaking user) explore freely within guardrails | Agents find ≥1 defect the scripted suite missed |
| A4 | **Oracle agents:** Agents verify AI features (Genie answers vs ground truth, extraction vs golden set) | Metrics dashboard produced per run |
| A5 | **Orchestrated multi-agent run in CI:** Planner, executor, triager, and reporter agents; auto-filed bug artifacts in Git | Nightly run publishes a report PR |

### 6.3 Agent design requirements
- Structured outputs (JSON schema) for steps, evidence (screenshots/HAR/trace), verdict, and confidence
- Deterministic replay: store prompts, model version, seed/temperature, and traces for every run
- Guardrails: domain allow-list, action allow-list (no account deletion, no payment), spending and rate caps, kill switch
- Triage step to de-duplicate and rate-limit bug filing (LLM false positives are the main risk)
- Metrics: defects found, false-positive rate, cost per run, run-to-run variance, coverage vs scripted suite

## 7. Test Environment and Data

| Item | Plan |
|------|------|
| Environments | Production (read-mostly, own tenant). Request staging if available |
| Tenants | `eva-qa-<n>.evalytics.in` (own trial academy; ask owner for upgraded limits) |
| Accounts | 1 owner, 2 teachers (one pending), 6+ students across 2 tenants for isolation tests |
| Email | Plus-addressed Gmail or a disposable test inbox with API (e.g., Mailosaur / MailHog equivalent) |
| Data | Synthetic only. Golden PDFs. No real student data |
| Devices/browsers | Chrome, Firefox, Safari/WebKit, Edge; Android Chrome and iOS Safari (real or emulated) |
| Observability | Playwright traces, HAR, video on failure; Git-stored run artifacts (summaries, not heavy binaries; use Git LFS or release assets for large files) |
| Time handling | Scheduling tests need clock awareness (IST vs browser time zone, DST for non-IST testers) |

## 8. Git-Based "JIRA" Model

Everything lives in one repo (or a small mono-repo). Issues are files, so history, review, and traceability come for free. If you also use GitHub Issues/Projects, mirror these files via a sync script; that is itself a good showcase item.

### 8.1 Proposed repository layout

```
evalytics-qa/
├── README.md
├── docs/
│   ├── test-plan/TEST-PLAN.md            # this document
│   ├── test-plan/ESTIMATES.md            # (generated from backlog)
│   ├── governance/AUTHORIZATION.md
│   ├── risk-register.md
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
│   ├── ai-eval/                          # golden datasets, scorers
│   └── agents/                           # agent harness, prompts, guardrails
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
| Board | `README` table or GitHub Project | n/a | Columns: Backlog, Ready, In Progress, In Review, Done |
| Workflow transition | PR merge + `status` field | n/a | Status changes via PR |

### 8.3 Sample story (template)

```markdown
---
id: EVA-S0012
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
- **Branching:** trunk-based with short-lived branches: `feat/EVA-S0012-autosubmit-test`, `fix/…`, `docs/…`
- **Commits:** Conventional Commits, referencing IDs: `test(exam): add auto-submit deadline spec [EVA-S0012]`
- **PRs:** required template (linked item, evidence, flake check); CI must pass; self-review checklist as a solo practitioner
- **Tags/releases:** `sprint-NN` tags at sprint end; `sut-v1.1.0-baseline` for the first baseline run
- **Definition of Ready:** acceptance criteria written, estimate present, data/accounts available
- **Definition of Done:** code/test reviewed and merged, runs green 3 consecutive times, traceability links updated, docs updated, artifacts in `reports/`

## 9. Work Breakdown and Estimates (Man-Hours)

**Method:** Bottom-up three-point estimate per epic (expected = (O + 4M + P) / 6), then a single sanity check against the capacity. The numbers below are **planning estimates before authenticated reconnaissance**. They will be re-baselined after Sprint 0, and the plan expects roughly ±25% accuracy at this stage.

**Assumptions:** one primary QA engineer (you), AI coding assistants available, access to an upgraded trial or staging tenant, no blocking environment issues.

| Epic | Description | Hours |
|------|-------------|------:|
| EVA-E01 | Project setup: repo, templates, CI skeleton, conventions | 10 |
| EVA-E02 | Discovery and recon (authenticated walkthrough, endpoint mapping, sitemap, data model guesses) | 16 |
| EVA-E03 | Test design: cases, charters, traceability matrix, risk register | 32 |
| EVA-E04 | Environment and test data: tenants, accounts, mailbox, golden PDFs | 14 |
| EVA-E05 | Exploratory and manual baseline testing, defect reporting | 36 |
| EVA-E06 | Automation framework: Playwright, fixtures, page objects, reporters, CI | 36 |
| EVA-E07 | UI functional automation (M01-M04, M08-M12, M15-M17) | 56 |
| EVA-E08 | API/network layer testing | 24 |
| EVA-E09 | Security testing (authorized, non-destructive): authn/z, tenant isolation, session, lockout | 28 |
| EVA-E10 | AI feature quality (extraction, explanations, equation converter, Genie) | 40 |
| EVA-E11 | Multilingual / i18n | 12 |
| EVA-E12 | Cross-browser, responsive/mobile, accessibility | 20 |
| EVA-E13 | Performance and resilience (light) | 18 |
| EVA-E14 | **AI-agent testing layer** (A1-A5) | 64 |
| EVA-E15 | Reporting, dashboards, case study / showcase write-up | 20 |
| EVA-E16 | Agile ceremonies and project management (~2.5h/week) | 24 |
| | **Subtotal** | **450** |
| | Contingency (15%) | 68 |
| | **Total** | **≈ 518 h** |

### 9.1 Duration by capacity

| Weekly productive hours | Calendar duration | 2-week sprints |
|------------------------:|------------------:|---------------:|
| 15 h (side project) | ~35 weeks | ~17 |
| 20 h | ~26 weeks | ~13 |
| 30 h | ~17 weeks | ~9 |
| 40 h (full-time) | ~13 weeks | ~7 |

### 9.2 Effort distribution
~12% planning/design, ~25% framework and automation, ~20% AI-feature and security testing, ~12% agents (post-baseline), plus the remainder in exploratory, reporting, and PM. Agents are deliberately built **after** the scripted baseline exists, so you have a ground truth to measure them against.

### 9.3 Estimate-reduction levers
- AI-assisted test authoring (can shave 15-25% off E03, E07)
- Descoping performance (E13) and a11y depth if the showcase focus is agents
- Reusing community Playwright MCP / agent frameworks instead of building a harness from scratch (E14)

## 10. Proposed Sprint Roadmap (30 h/week example, 2-week sprints)

| Sprint | Theme | Key outputs |
|--------|-------|-------------|
| **S0** | Foundations and recon | Repo, authorization note, tenants, sitemap, endpoint map, refined estimates, risk register v1 |
| **S1** | Test design + manual baseline | Traceability matrix, 60+ cases, first exploratory sessions, first bug reports |
| **S2** | Automation framework + P0 smoke | CI green, auth + enrollment + academy creation smoke suite |
| **S3** | P0/P1 functional automation | Question bank, paper builder, scheduling, exam taking, results |
| **S4** | Security + API | Isolation and authz test suite, API checks, findings report (private) |
| **S5** | AI-feature evaluation | Golden dataset, scorers, extraction/Genie/translation metrics |
| **S6** | i18n, cross-browser, a11y, light perf | Compatibility matrix, WCAG findings |
| **S7** | Agents A1-A3 | Agent harness, charter execution, persona exploration, comparison to scripted suite |
| **S8** | Agents A4-A5 + hardening | Oracle agents, nightly CI run, flake reduction |
| **S9** | Showcase | Final report, dashboards, case-study post, demo video, retro |

Re-plan every sprint using actual velocity (hours completed vs planned).

## 11. Entry and Exit Criteria

**Entry (per phase):** environment reachable, test accounts provisioned, authorization on file, stories Ready.

**Exit (overall):**
- 100% of P0 and ≥90% of P1 stories executed, with results traceable to requirements
- No open Critical/High defects without an agreed disposition
- Automated regression suite stable (<5% flaky across 10 runs)
- AI-feature metrics reported with sample sizes and confidence notes
- Agent benchmark report: coverage, defects, false-positive rate, cost
- All artifacts committed, sprints closed with review and retro

## 12. Defect Management

- Severity: S1 Critical (data leak, wrong score, exam lost), S2 High, S3 Medium, S4 Low
- Required fields: ID, title, environment/version, steps, expected/actual, evidence, severity/priority, linked test case
- Security findings go to a **private** `security/` folder or private repo, with coordinated disclosure to the owner before anything is published in the showcase. Redact tenant specifics in public write-ups.

## 13. Metrics and Reporting

Requirement/risk coverage, pass rate by run, defect density and escape analysis, automation ROI (hours saved vs invested), flake rate, mean time to detect for agents vs scripts, agent false-positive rate, cost per agent run, sprint velocity and burndown.

## 14. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Testing against production affects real users | Med | High | Own tenant, throttling, staging request, off-peak runs |
| Trial AI quotas too small for evaluation | High | Med | Request upgraded limits; stratified small samples |
| Authorization scope ambiguity (security testing) | Med | High | Written scope; non-destructive only |
| Email-dependent flows are hard to automate | Med | Med | Mailbox API, plus-addressing |
| Time-based flows are slow/flaky | High | Med | Short exam windows in QA tenant; server-time assertions |
| LLM agent false positives and nondeterminism | High | Med | Structured verdicts, evidence, triage agent, replay logs |
| Bot protection / rate limiting blocks automation | Med | Med | Coordinate allow-listing with owner |
| SUT changes during project (v1.1.0 to later) | High | Med | Version-tag every run; keep tests resilient (roles/test-ids) |
| Scope creep | Med | Med | Sprint-gated backlog, change log in ADRs |

## 15. Open Questions (to resolve in Sprint 0)

1. Is there a staging/sandbox environment, and can your tenant be upgraded for AI-quota and seat testing?
2. What security test types are explicitly permitted (brute-force lockout, IDOR probes, passive scanning)?
3. Is billing/payment live in the trial flow, and should it be tested?
4. Is there API documentation (OpenAPI), given the "API access" plan feature?
5. Which LLM(s) and agent framework do you want to use for the agent layer (e.g., Claude via API with Playwright MCP)?
6. Is the repo public or private? This determines how findings are published.
7. Which weekly capacity should the plan be committed to (Section 9.1)?

## 16. Traceability Seeds

Each module (M01-M18) becomes at least one Epic-linked story set. Each story links to test cases (`EVA-TC####`) and each test case to automation file paths and agent charters, so the matrix `module → story → test case → automated/agent coverage` can be generated by script from front matter. This generator is itself a portfolio-worthy deliverable.

## 17. Revision History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 0.1.0 | 2026-11-14 | <your-name> | Initial draft from public-page recon |
