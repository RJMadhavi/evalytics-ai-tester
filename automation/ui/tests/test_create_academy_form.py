"""Checks of the sign-up form at /create-academy. Story EVA-S0022.

Part 1 only types into fields and reads the page. It never submits, so it is read-only.
Part 2 submits invalid forms. It is skipped unless EVA_ALLOW_FORM_SUBMIT=1 and
EVA_TEST_EMAIL is set, which you do only after the owner approves in writing.
"""
import os
import re

import pytest
from playwright.sync_api import expect

from common.guardrails import require_invalid_academy_form
from pages.create_academy_page import SUBJECTS, CreateAcademyPage


@pytest.fixture
def form(page):
    f = CreateAcademyPage(page)
    f.open()
    return f


# ---------------------------------------------------------------- part 1: read-only

FIELDS = ("academy_name", "subdomain", "full_name", "subject", "email", "password", "confirm_password")


@pytest.mark.parametrize("field", FIELDS)
def test_every_field_has_an_accessible_label(form, field):
    expect(getattr(form, field)).to_have_count(1)


@pytest.mark.parametrize("field", ("password", "confirm_password"))
def test_password_fields_are_masked(form, field):
    expect(getattr(form, field)).to_have_attribute("type", "password")


def test_subject_list_has_the_ten_subjects(form):
    options = [o.strip() for o in form.subject.locator("option").all_inner_texts()]
    assert "select" in options[0].lower(), f"first option should be the placeholder, got {options[0]!r}"
    assert tuple(options[1:]) == SUBJECTS


def test_subdomain_preview_follows_typing(form):
    form.subdomain.fill("my-qa-test")
    expect(form.preview).to_contain_text("my-qa-test.evalytics.in")


@pytest.mark.parametrize("typed", ["My QA_Academy!", "UPPER", "with space"])
def test_preview_only_shows_allowed_characters(form, typed):
    """The label says: lowercase letters, numbers, hyphens only. If this fails, look at
    the page by hand before calling it a bug (the field may reject the keystrokes)."""
    form.subdomain.fill(typed)
    text = form.preview.inner_text()
    match = re.search(r"([^\s\U0001F310]+)\.evalytics\.in", text)
    assert match, f"no address found in preview: {text!r}"
    assert re.fullmatch(r"[a-z0-9-]+", match.group(1)), f"preview shows {match.group(1)!r}"


@pytest.mark.xfail(
    reason="REC-02b: Terms of Service and Privacy Policy links are placeholders ('#')",
    strict=True,
)
@pytest.mark.parametrize("link", ("terms_link", "privacy_link"))
def test_legal_links_lead_somewhere(form, link):
    href = getattr(form, link).get_attribute("href")
    assert href and href != "#"


# ---------------------------------------------------------------- part 2: submits

SUBMIT_OK = os.environ.get("EVA_ALLOW_FORM_SUBMIT") == "1"
TEST_EMAIL = os.environ.get("EVA_TEST_EMAIL", "")  # one of your own test addresses, e.g. box+autotest@gmail.com
GOOD = {"name": "ZZ Autotest Delete Me", "sub": "zz-autotest-delete-me", "full": "Auto Test", "pw": "Passw0rd!Aa1"}

# Only obvious faults, so the app is very unlikely to accept them.
CASES = {
    "empty academy name": ("", GOOD["sub"], GOOD["full"], "{email}", GOOD["pw"], GOOD["pw"]),
    "empty subdomain": (GOOD["name"], "", GOOD["full"], "{email}", GOOD["pw"], GOOD["pw"]),
    "empty full name": (GOOD["name"], GOOD["sub"], "", "{email}", GOOD["pw"], GOOD["pw"]),
    "invalid email": (GOOD["name"], GOOD["sub"], GOOD["full"], "not-an-email", GOOD["pw"], GOOD["pw"]),
    "passwords differ": (GOOD["name"], GOOD["sub"], GOOD["full"], "{email}", GOOD["pw"], "Different1!Zz"),
    "empty password": (GOOD["name"], GOOD["sub"], GOOD["full"], "{email}", "", ""),
}


@pytest.mark.writes_ok
@pytest.mark.skipif(
    not SUBMIT_OK,
    reason="Form submissions need the owner's written approval. Set EVA_ALLOW_FORM_SUBMIT=1 once approved.",
)
@pytest.mark.parametrize("case", list(CASES), ids=list(CASES))
def test_invalid_submission_is_rejected(form, page, case):
    if not TEST_EMAIL:
        pytest.skip("Set EVA_TEST_EMAIL to one of your own test addresses first.")
    fields = tuple(v.replace("{email}", TEST_EMAIL) for v in CASES[case])
    require_invalid_academy_form(*fields)  # refuses if the form could create a real academy
    form.fill(*fields)
    form.submit_button.click()
    page.wait_for_load_state("networkidle")
    expect(page.get_by_text("Registration Received")).to_have_count(0)
    expect(page).to_have_url(re.compile(r"/create-academy"))
