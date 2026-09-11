"""
Test Academy Login
"""

from data.config import (
    ACADEMY_1_BASE_URL,
    ACADEMY_1_USERNAME,
    ACADEMY_1_PASSWORD,
)

from pages.auth.login_page import LoginPage


def test_academy_1_login(page):

    assert ACADEMY_1_BASE_URL, (
        "ACADEMY_1_BASE_URL is not configured in .env"
    )

    assert ACADEMY_1_USERNAME, (
        "ACADEMY_1_USERNAME is not configured in .env"
    )

    assert ACADEMY_1_PASSWORD, (
        "ACADEMY_1_PASSWORD is not configured in .env"
    )

    login_page = LoginPage(page)

    login_page.open(
        ACADEMY_1_BASE_URL
    )

    login_page.login(
        username=ACADEMY_1_USERNAME,
        password=ACADEMY_1_PASSWORD,
    )

    assert login_page.is_logged_in(), (
        "Academy login failed"
    )