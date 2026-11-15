# Evalytics QA: Agile Test Project with AI-Agent Testing

[![CI](https://github.com/<your-username>/evalytics-qa/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/evalytics-qa/actions)
![Status](https://img.shields.io/badge/status-Sprint%200-blue)
![SUT](https://img.shields.io/badge/SUT-Evalytics%20v1.1.0-lightgrey)

A QA engineering portfolio project that tests [Evalytics](https://evalytics.in), an AI-powered online exam portal for coaching academies. The project covers functional, API, security, AI-quality, i18n, accessibility and light performance testing, and ends with **autonomous AI agents that test the application** and are benchmarked against a scripted suite.

> **Authorization:** This testing is performed with the written permission of the Evalytics owner. See [`docs/governance/AUTHORIZATION.md`](docs/governance/AUTHORIZATION.md) for scope and permitted test types. Testing is limited to my own QA academy tenant using synthetic data only. No real student data is accessed, stored or published.

## Goals

| # | Goal | Success measure |
|---|------|-----------------|
| G1 | Establish a functional, API, security and non-functional baseline | Risk-based coverage report with triaged defects |
| G2 | Build a maintainable automation framework | Green CI, <5% flaky tests |
| G3 | Deploy AI agents that test the app | Agents run charters, file reproducible bug reports, benchmarked against scripted tests |
| G4 | Showcase engineering and process skill | Plan, estimates, traceability, dashboards, write-up |

## How this project works

The repo is a Git-based "Jira": every work item is a Markdown file with YAML front matter, changed through pull requests.

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

Work is organised in 2-week Scrum-style sprints. Each sprint has a plan, review, retro and burndown under `sprints/`. Commits follow Conventional Commits and reference item IDs, for example `test(exam): add auto-submit deadline spec [EVA-S0012]`.

## Repository layout

```
docs/          Test plan, estimates, governance, risk register, ADRs
backlog/       Epics, stories, tasks, bugs, spikes
sprints/       Per-sprint plan, review, retro, burndown
test-cases/    Manual and automated case specifications
charters/      Exploratory and agent charters
automation/
  ui/          Playwright (TypeScript) UI tests
  api/         API and contract tests
  ai-eval/     Golden datasets and scorers for AI features
  agents/      Agent harness, prompts, guardrails
reports/       Run summaries and dashboards
.github/       Issue/PR templates and CI workflows
```

## Test approach at a glance

- **Risk-based:** tenant isolation, exam timing and scoring, and authentication are P0.
- **Layers:** exploratory (SBTM), UI, API, security (authorized, non-destructive), AI quality, i18n, cross-browser, accessibility, light performance.
- **AI features:** non-deterministic output is evaluated with golden datasets, rubric scoring and metamorphic tests rather than exact-match assertions.
- **AI agents:** built in stages (A1 to A5) after the scripted baseline exists, so there is ground truth to measure them against.

Full detail: [`docs/test-plan/TEST-PLAN.md`](docs/test-plan/TEST-PLAN.md)

## Agent testing roadmap

| Stage | Description | Status |
|-------|-------------|--------|
| A1 | Agent-assisted test authoring | Not started |
| A2 | Agent-executed scripted charters | Not started |
| A3 | Persona-based exploratory agents | Not started |
| A4 | Oracle agents for AI features (Genie, extraction) | Not started |
| A5 | Orchestrated multi-agent nightly run in CI | Not started |

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
| S6 | i18n, cross-browser, a11y, light perf | Planned |
| S7 | Agents A1 to A3 | Planned |
| S8 | Agents A4 to A5 and hardening | Planned |
| S9 | Showcase | Planned |

Estimated effort: about 518 hours including 15% contingency. See the test plan, section 9. Estimates are re-baselined after Sprint 0.

## Getting started

> Setup instructions will be filled in during Sprint 2, once the framework exists.

```bash
git clone https://github.com/<your-username>/evalytics-qa.git
cd evalytics-qa
# npm install && npx playwright install      (UI tests)
# pip install -r automation/ai-eval/requirements.txt   (AI evaluation)
cp .env.example .env    # add your QA tenant URL and test credentials
```

Never commit credentials. `.env` is git-ignored.

## Responsible testing

- Only my own QA tenant is tested, with synthetic data and dedicated test mailboxes.
- Automation is throttled to avoid affecting real users.
- Heavy, security and load testing run on staging if available.
- Security findings are kept private and disclosed to the owner before anything is published. Public write-ups redact tenant-specific details.

## Documentation

- [Master Test Plan](docs/test-plan/TEST-PLAN.md)
- [Authorization and scope](docs/governance/AUTHORIZATION.md)
- [Risk register](docs/risk-register.md)
- [Architecture decision records](docs/adr/)

## About

Built by **<your-name>** as a QA portfolio project. Connect on [LinkedIn](<your-linkedin-url>).

This project is independent. It is not an official Evalytics repository, and test findings reflect the SUT at the version noted in each run.

## License

Test code and documentation are released under the MIT License (see `LICENSE`). This license does not cover the Evalytics application or its content.
