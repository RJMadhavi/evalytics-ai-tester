# Evalytics QA: Agile Test Project

[![CI](https://github.com/<your-username>/evalytics-ai-tester/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/evalytics-ai-tester/actions)
![Status](https://img.shields.io/badge/status-Sprint%200-blue)
![SUT](https://img.shields.io/badge/SUT-Evalytics%20v1.1.0-lightgrey)

This project tests [Evalytics](https://evalytics.in), an AI-powered online exam portal for coaching academies. It combines manual and automated testing across functional, API, security, performance, accessibility and AI-quality areas, and finishes by setting up AI agents that test the application.

> **Authorization:** Testing is performed with the written permission of the Evalytics owner. See [`docs/governance/AUTHORIZATION.md`](docs/governance/AUTHORIZATION.md) for scope and permitted test types. Testing is limited to my own QA academy tenant using synthetic data only. No real student data is accessed, stored or published.

## Goals

1. **Functional testing:** verify every module of the app against its documented behaviour.
2. **Unit testing (if possible):** the app's source code is not available, so unit tests apply only if the owner shares code or components. Otherwise, this covers unit tests for this repo's own test utilities, scorers and agent code.
3. **Load testing:** measure behaviour under expected concurrent use, such as a class taking an exam at once. Run on staging, or within limits the owner approves in writing.
4. **Stress testing:** find where the app degrades as load grows beyond normal. Same restrictions as load testing, and never against production without approval.
5. **Security testing:** authorized and non-destructive checks of authentication, authorization, session handling, lockout and tenant isolation.
6. **Testing the underlying AI functionality:** question extraction, explanations, equation conversion, translation and the Genie assistant, evaluated with golden datasets and rubrics.
7. **Accessibility testing:** WCAG 2.2 AA checks, automated and manual, including keyboard and screen-reader use.
8. **API testing:** contract, negative and authorization tests on the endpoints the app uses.
9. **AI agents for testing:** set up agents that test the existing features and also pick up new ones as the app changes, and benchmark them against the scripted tests.

## How this project works

The repo is a Git-based "Jira": every work item is a Markdown file with YAML front matter, changed through pull requests. Sprints are tracked on the **EvalyticsQA** GitHub Project board.

| Jira concept | Where it lives | ID |
|--------------|----------------|----|
| Epic | `backlog/epics/` | `EVA-E##` |
| Story | `backlog/stories/` | `EVA-S####` |
| Task | `backlog/tasks/` | `EVA-T####` |
| Bug (defect in the SUT) | `backlog/bugs/` | `EVA-B####` |
| Spike | `backlog/spikes/` | `EVA-SP####` |
| Test case | `test-cases/` | `EVA-TC####` |
| Test run | `reports/runs/` | `EVA-TR####` |
| Sprint | `sprints/sprint-NN/` | `S##` |

Work is organised in 2-week Scrum-style sprints, each with a plan, review, retro and burndown under `sprints/`. Commits follow Conventional Commits and reference item IDs, for example `test(exam): add auto-submit deadline spec [EVA-S0012]`.

## Repository layout

```
docs/          Test plan, estimates, governance, risk register, ADRs
backlog/       Epics, stories, tasks, bugs, spikes
sprints/       Per-sprint plan, review, retro, burndown
test-cases/    Manual and automated case specifications
charters/      Exploratory and agent charters
automation/
  ui/          Playwright UI tests
  api/         API and contract tests
  performance/ Load and stress scripts
  ai-eval/     Golden datasets and scorers for AI features
  agents/      Agent harness, prompts, guardrails
reports/       Run summaries and dashboards
.github/       Issue/PR templates and CI workflows
```

## Test approach at a glance

- **Risk-based:** tenant isolation, exam timing and scoring, and authentication are the highest priority.
- **AI features:** non-deterministic output is evaluated with golden datasets, rubric scoring and metamorphic tests rather than exact-match assertions.
- **Performance:** load and stress tests are small, scripted and throttled, and run only where the owner has approved it.
- **AI agents:** built in stages after the scripted baseline exists, so there is ground truth to measure them against.

Full detail: [`docs/test-plan/TEST-PLAN.md`](docs/test-plan/TEST-PLAN.md)

## Agent testing roadmap

| Stage | Description | Status |
|-------|-------------|--------|
| A1 | Agent-assisted test authoring | Not started |
| A2 | Agent-executed scripted charters | Not started |
| A3 | Persona-based exploratory agents | Not started |
| A4 | Oracle agents for AI features (Genie, extraction) | Not started |
| A5 | Orchestrated multi-agent nightly run in CI, including checks on newly released features | Not started |

Agent guardrails: domain allow-list, action allow-list (no account deletion or payment), rate and spend caps, kill switch, observe-and-report only.

## Project status

| Sprint | Theme | Status |
|--------|-------|--------|
| S0 | Foundations and recon | In progress |
| S1 | Test design and manual baseline | Planned |
| S2 | Automation framework and P0 smoke | Planned |
| S3 | P0/P1 functional automation | Planned |
| S4 | Security and API | Planned |
| S5 | AI-feature evaluation | Planned |
| S6 | i18n, cross-browser, accessibility | Planned |
| S7 | Load and stress testing | Planned |
| S8 | Agents A1 to A3 | Planned |
| S9 | Agents A4 to A5 and hardening | Planned |

Estimates are re-baselined after Sprint 0. See the test plan, section 9.

## Responsible testing

- Only my own QA tenant is tested, with synthetic data and dedicated test mailboxes.
- Automation is throttled to avoid affecting real users.
- Load, stress and security testing run on staging if available, or within limits agreed in writing with the owner.
- Security findings are kept private and disclosed to the owner before anything is published. Public write-ups redact tenant-specific details.

## Documentation

- [Master Test Plan](docs/testplan/TEST-PLAN.md)
- [Authorization and scope](docs/governance/AUTHORIZATION.md)
- [Risk register](docs/risk-register.md)
- [Architecture decision records](docs/adr/)

## About

Built by **Madhavi Joshi**. This project is independent and is not an official Evalytics repository. Test findings reflect the app at the version noted in each run.

## License

Test code and documentation are released under the MIT License (see `LICENSE`). This license does not cover the Evalytics application or its content.
