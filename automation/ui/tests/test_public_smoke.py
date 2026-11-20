"""Read-only checks of the public pages. Story EVA-S0021.

Nothing here logs in or submits a form. Write requests are blocked by conftest.py."""
import re

import pytest
from playwright.sync_api import expect

from common.guardrails import tracker_hosts
from pages.create_academy_page import CreateAcademyPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.pricing_page import PLANS, PricingPage

PAGES = [HomePage, PricingPage, LoginPage, CreateAcademyPage]
IDS = [p.path for p in PAGES]


@pytest.mark.parametrize("page_cls", PAGES, ids=IDS)
def test_page_loads_with_evalytics_title(page, page_cls):
    response = page_cls(page).open()
    assert response is not None and response.ok, f"{page_cls.path} returned {response and response.status}"
    assert "Evalytics" in page.title()


@pytest.mark.parametrize("page_cls", PAGES, ids=IDS)
def test_footer_shows_a_version(page, page_cls, run_notes):
    pg = page_cls(page)
    pg.open()
    version = pg.footer_version()
    assert version, f"no version string like v1.2.3 found on {page_cls.path}"
    run_notes["versions"].add(version)


@pytest.mark.parametrize("page_cls", PAGES, ids=IDS)
def test_no_console_errors(page, page_cls, console_errors):
    page_cls(page).open()
    page.wait_for_load_state("networkidle")
    assert not console_errors, console_errors


@pytest.mark.parametrize("page_cls", PAGES, ids=IDS)
def test_no_known_trackers(page, page_cls, seen_hosts):
    """Checks the claim 'zero third-party trackers' (claim C2 in docs/recon/public-pages.md)."""
    page_cls(page).open()
    page.wait_for_load_state("networkidle")
    assert tracker_hosts(seen_hosts) == [], f"tracker hosts contacted: {tracker_hosts(seen_hosts)}"


def test_pricing_lists_all_plans_and_trial(page):
    PricingPage(page).open()
    body = page.locator("body")
    for plan in PLANS:
        expect(body).to_contain_text(plan)
    expect(body).to_contain_text(re.compile(r"15[- ]day", re.I))


def test_login_page_has_email_password_and_button(page):
    login = LoginPage(page)
    login.open()
    expect(login.email).to_be_visible()
    expect(login.password).to_be_visible()
    expect(login.sign_in).to_be_visible()


def test_header_pricing_link_goes_to_pricing(page):
    HomePage(page).open()
    page.get_by_role("link", name=re.compile("pricing", re.I)).first.click()
    expect(page).to_have_url(re.compile(r"/pricing"))
