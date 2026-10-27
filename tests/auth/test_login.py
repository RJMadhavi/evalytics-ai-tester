"""
Test Academy Login (approved account)
"""
import pytest

from pages.auth.login import LoginPage

pytestmark = [pytest.mark.accounts]


def test_academy_1_login(page, academy_1_credentials):
    login_page = LoginPage(page)

    login_page.open(academy_1_credentials["base_url"])

    login_page.login(
        username=academy_1_credentials["username"],
        password=academy_1_credentials["password"],
    )

    assert login_page.is_logged_in(), "Academy login failed"
