# Evalytics AI Tester

Test automation framework for the [Evalytics](https://evalytics.in) platform —
a multi-tenant academy application (student exams, teacher portals, academy
administration).

Built with **pytest + Playwright** using the Page Object Model, data
factories, and a safety system that keeps destructive tests away from
production.

## Quick start

```bash
uv venv .venv --python 3.12          # or: python -m venv .venv
VIRTUAL_ENV=$PWD/.venv uv pip install -r requirements.txt
.venv/bin/playwright install chromium

cp .env.example .env                 # fill in your target + accounts
.venv/bin/python -m pytest          # run everything
```

## Test categories

The suite is split by **risk**, selected with markers:

| Marker | What it does | Safe against production? | Runs in CI? |
|---|---|---|---|
| `smoke` | Read-only checks of public pages | Yes | Every PR + scheduled agent |
| `unit` | Data-factory tests, no browser | Yes | Every PR |
| `accounts` | Login + settings using approved academy accounts | Read-mostly | Only with secrets |
| `mutating` | Creates academies/students | **No** | Only with explicit opt-in |

```bash
.venv/bin/python -m pytest -m smoke       # read-only, safe anywhere
.venv/bin/python -m pytest -m unit         # fast, no browser
.venv/bin/python -m pytest -m accounts     # needs approved credentials
.venv/bin/python -m pytest                 # everything (mutating gated)
```

### The safety gate

Tests marked `@pytest.mark.mutating` are **skipped automatically** unless
`EVALYTICS_AUTOMATION_ENABLED=true` is set, and should only ever target a
disposable environment. Production may only be used for read-only smoke
checks. Failed browser tests save a Playwright trace to `test-results/`
(open with `.venv/bin/playwright show-trace <file>.zip`).

## Repository layout

```
conftest.py               # fixtures + the mutating-test safety gate
data/
  config.py               # reads .env / CI secrets
  factories/              # Faker-based test data generators
  reporting.py            # JSON reports of created academies
pages/                    # Page Objects (auth, academy, student)
tests/
  smoke/                  # read-only public-page checks
  auth/ academy/ student/ # journey tests (gated)
  email/                  # Mailpit helper script
.github/workflows/
  ci.yml                  # PR gate: lint, unit, smoke
  smoke-agent.yml          # scheduled "testing agent" + failure issues
  integration.yml         # manual full-suite runs (secrets required)
```

## CI/CD

- **Every push/PR** — `ci.yml` runs lint, unit tests, and the read-only
  smoke suite. No secrets needed.
- **Every 6 hours** — `smoke-agent.yml` (the *Smoke Agent*) checks the
  website, publishes a Markdown report in the job summary, uploads the
  report + failure traces, and opens a GitHub issue if the site is broken.
- **On demand** — `integration.yml` runs the full suite, including
  data-creating tests, against an environment you approve. Requires the
  repository secrets listed in the workflow file.

New to CI/CD? Work through [LEARNING.md](LEARNING.md) — it explains every
piece of this repo with hands-on exercises.

## Learning resources

- [LEARNING.md](LEARNING.md) — test automation + CI/CD curriculum built
  around this repository.
- `docs/` — the test strategy and test inventory that drive this suite.
