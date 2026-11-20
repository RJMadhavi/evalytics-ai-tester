# Automation

Python and Playwright tests for Evalytics, written to the safety rules in the test plan (section 2).

## Layout

```
automation/
  common/       Shared safety rules (guardrails.py) and their unit tests
  ui/           Browser tests: page objects, tests, tools
  pytest.ini
  requirements.txt
```

## Set up (Codespace or Terminal)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r automation/requirements.txt
playwright install --with-deps chromium     # in a Codespace
# playwright install chromium               # on a Mac
cd automation
```

## Run

```bash
pytest common                                  # unit tests only, never touches the website
pytest ui --screenshot only-on-failure --tracing retain-on-failure
```

Open a trace with `playwright show-trace <file>.zip`. Run summaries go to `reports/runs/<date>/ui-summary.json`.

## Safety defaults

| Rule | How it works |
|------|--------------|
| Allow-list | Page navigations to hosts outside `evalytics.in` and `EVA_ALLOWED_HOSTS` are blocked and fail the test |
| Read-only | POST, PUT, PATCH and DELETE are blocked unless the test is marked `@pytest.mark.writes_ok` |
| Throttle | One page navigation per second by default (`EVA_MIN_INTERVAL`) |
| Kill switch | Set `EVA_KILL=1` or create the file `.local/KILL`. The run stops before the next test. |
| No accidental sign-ups | `require_invalid_academy_form()` refuses to submit a form that looks valid |

Set your own academies, never anyone else's, with exact names:

```bash
export EVA_ALLOWED_HOSTS="yourqa1.evalytics.in,yourqa2.evalytics.in"
```

Do not mark a test `writes_ok` until the owner's written approval covers it (`docs/governance/AUTHORIZATION.md`).

## Find the real form fields

```bash
python3 ui/tools/dump_form.py /create-academy
```

It only reads the page. Paste the output to finish the page object and write the form validation tests.

## Form tests (S0022)

`ui/tests/test_create_academy_form.py` has two parts:

1. Read-only checks that type into the form but never submit it. They run with everything else.
2. Submit checks for invalid forms. They are **skipped** unless you set both of these in your own terminal, and only after the owner has approved form submissions in writing:

```bash
export EVA_ALLOW_FORM_SUBMIT=1
export EVA_TEST_EMAIL="yourbox+autotest@gmail.com"   # one of your own test addresses
```

The test data is named `ZZ Autotest Delete Me` so the owner can spot and delete it if the app ever accepts one by mistake.
