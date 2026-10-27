"""
Read-only smoke tests for the public Evalytics website.

These tests only GET public pages and verify content — they never
create or modify data, so they are safe to run against any
environment, including production, and from CI without secrets.
"""
import pytest

pytestmark = [pytest.mark.smoke]


PUBLIC_PAGES = [
    ("/", "home"),
    ("/login", "login"),
    ("/pricing", "pricing"),
    ("/register", "register"),
    ("/create-academy", "create-academy"),
]


def test_home_page_renders(page, target_base_url):
    page.goto(target_base_url)
    page.wait_for_load_state("domcontentloaded")

    assert "Evalytics" in page.title()
    assert page.locator("body").inner_text().strip() != ""


def test_login_page_shows_form(page, target_base_url):
    page.goto(f"{target_base_url}/login")

    assert page.locator("#email").is_visible()
    assert page.locator("#password").is_visible()


def test_pricing_page_offers_plans(page, target_base_url):
    page.goto(f"{target_base_url}/pricing")

    body = page.locator("body").inner_text().lower()
    assert any(
        word in body for word in ("plan", "pricing", "month")
    ), "Pricing page does not appear to show plans"


def test_create_academy_page_renders_form(page, target_base_url):
    page.goto(f"{target_base_url}/create-academy")

    # The public academy signup form
    assert page.get_by_role(
        "button", name="Create Academy"
    ).is_visible()


def test_unknown_route_shows_404(page, target_base_url):
    page.goto(f"{target_base_url}/this-page-does-not-exist-qa")
    page.wait_for_load_state("domcontentloaded")

    assert "404" in page.locator("body").inner_text(), (
        "Unknown route did not render the 404 page"
    )


@pytest.mark.parametrize("path,name", PUBLIC_PAGES)
def test_public_page_returns_ok(page, target_base_url, path, name):
    response = page.request.get(f"{target_base_url}{path}")

    assert response.status == 200, (
        f"{name} ({path}) returned {response.status}, expected 200"
    )
