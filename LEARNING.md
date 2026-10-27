# Learning Path: Test Automation + CI/CD

This guide teaches test automation and CI/CD using **this repository** —
every lesson is something you can actually run. Budget ~30 minutes per
lesson. Keep a notebook of what you observe; the exercises are where the
real learning happens.

---

## Part 1 — Running and reading tests

### Lesson 1.1: Run one test and read it

```bash
.venv/bin/python -m pytest tests/smoke/test_public_pages.py::test_login_page_shows_form -v
```

Open `tests/smoke/test_public_pages.py` and answer:

- Where does the `page` fixture come from? *(pytest-playwright provides it —
  see how you never create a browser yourself.)*
- What does `page.locator("#email")` match? Open
  https://evalytics.in/login and find the element.
- Why is the assertion in the test and not in the page object?

### Lesson 1.2: Break a test on purpose

In `tests/smoke/test_public_pages.py`, change
`assert "Evalytics" in page.title()` to
`assert "NotARealSite" in page.title()`. Run:

```bash
.venv/bin/python -m pytest -m smoke
```

The test fails, and Playwright saves a trace (pytest.ini has
`--tracing retain-on-failure`). Open it:

```bash
.venv/bin/playwright show-trace test-results/<name>.zip
```

The trace viewer shows every action, screenshot, and network call — this
is your #1 debugging tool as a QA engineer. **Revert the change.**

**Exercise:** instead of breaking the assertion, break the selector
(`#emai`). Observe the difference: a selector failure fails *before* the
assertion. Learn to tell "app bug" from "test bug".

### Lesson 1.3: Markers and the safety gate

```bash
.venv/bin/python -m pytest --collect-only -q     # what would run?
.venv/bin/python -m pytest -q                    # note the skips
```

Read `conftest.py`: `pytest_collection_modifyitems` skips anything marked
`mutating` unless `EVALYTICS_AUTOMATION_ENABLED=true`. This is the
framework's most important idea — **tests that create data must never run
against production by accident**.

**Exercise:** run `EVALYTICS_AUTOMATION_ENABLED=true .venv/bin/python -m pytest -q`
and see the mutating tests *collect* but skip for missing accounts
instead. Why is that the correct behavior?

---

## Part 2 — Writing automation

### Lesson 2.1: Add a page-object method

Page Objects keep selectors in one place. Open `pages/auth/login.py` and
add:

```python
def error_message(self) -> str:
    return self.page.locator("body").inner_text()
```

### Lesson 2.2: Add a test

Create `tests/smoke/test_login_validation.py`:

```python
import pytest
from pages.auth.login import LoginPage

pytestmark = [pytest.mark.smoke]

def test_login_with_bad_credentials(page, target_base_url):
    login = LoginPage(page)
    login.open(target_base_url)
    login.login("nobody@nowhere.dev", "WrongPass!9")
    assert "login" in page.url.lower()   # still on the login page
```

Run it. Notice it never *creates* anything — safe to mark `smoke`.

**Exercise:** assert the actual error message appears. What text does the
site show for invalid credentials? (Hint: run it, then check the body
text with `print(page.inner_text("body"))`.)

### Lesson 2.3: Understand the data factory

Read `data/factories/tenant_data.py` and run:

```bash
.venv/bin/python -m pytest tests/test_tenant_data.py -v
```

The factory uses Faker with a **seed** — the same seed always produces the
same data. Why does determinism matter for debugging a failed run?

---

## Part 3 — CI/CD fundamentals

CI = every change is automatically built and tested. CD = good changes
are automatically deployed. This repo implements CI; CD belongs to the
application repo (it deploys, then this repo's tests act as the
post-deploy gate).

### Lesson 3.1: Read a workflow file

Open `.github/workflows/ci.yml`. Every GitHub Actions workflow is just:

- **Triggers** (`on:`) — when to run (push, PR, schedule, manual)
- **Jobs** — machines that run in parallel (`runs-on: ubuntu-latest`)
- **Steps** — shell commands and reusable actions (`uses:`)

Vocabulary to notice: *artifact*, *secret*, *job summary*, *matrix*.

### Lesson 3.2: Watch CI respond to a change

1. Create a branch: `git checkout -b learn-ci`
2. Break a smoke test (Lesson 1.2 style), commit, push, open a PR.
3. Watch the **Actions tab**: the PR gets red/green checks.
4. Read the failing job's log. Fix the test, push, watch it go green.

**This loop is the heart of CI.** Nothing else matters until this is
muscle memory.

### Lesson 3.3: Secrets and environments

Read `.github/workflows/integration.yml`. Secrets
(`Settings → Secrets and variables → Actions`) are encrypted values only
exposed to the jobs that request them — that's how credentials get into
CI without ever being committed. Notice the workflow **fails loudly when
secrets are missing** instead of silently passing. A green check must
always mean "it actually tested something".

**Exercise (setup):** add the secrets listed in `integration.yml` for a
staging environment when you have one.

---

## Part 4 — The "agents"

### Lesson 4.1: What the Smoke Agent actually is

Open `.github/workflows/smoke-agent.yml`. It is a **scheduled workflow**
(cron) that runs the smoke suite, publishes a report to the job summary,
uploads artifacts, and opens a GitHub issue on failure. That is honest
automation: deterministic checks, run like a monitoring agent.

The industry reality: an "AI test agent" is this same loop plus an LLM
step that reads the structured failure (junit XML, traces) and drafts a
triage. The scheduled workflow is the right foundation for it.

### Lesson 4.2: Trigger the agent manually

Actions tab → **Smoke Agent** → **Run workflow**. Read the summary it
publishes. Break the site expectation (e.g. point `TARGET_URL` at a
nonexistent URL) and see the failure issue appear.

---

## Part 5 — Where to go next

1. **More coverage:** port journey tests from the private Evalytics QA
   pack (exam taking, teacher flows) behind the `mutating` gate with a
   seeded staging environment.
2. **Performance:** add a scheduled k6 smoke (the load framework from the
   QA pack) — but only against staging, never production.
3. **CD:** in the *application* repo, make deploy → run this repo's smoke
   suite → promote. That's a real pipeline.
4. **AI triage:** add a workflow step that sends `smoke-results.xml` to
   an AI API for a first-draft diagnosis attached to the failure issue.

Concepts you now own: page objects, fixtures, markers, the safety gate,
traces, triggers/jobs/artifacts/secrets, scheduled agents, PR gating.
