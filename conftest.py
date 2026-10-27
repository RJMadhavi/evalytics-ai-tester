"""
Root conftest — shared fixtures and safety gates.

Framework rules:
- Tests marked ``@pytest.mark.mutating`` create data (academies,
  students, exams). They only run when EVALYTICS_AUTOMATION_ENABLED=true,
  and must never be pointed at production.
- Tests that need approved academy accounts skip themselves with a clear
  message when the accounts are not configured (instead of failing).
- Run with ``pytest --tracing retain-on-failure`` to get a Playwright
  trace for every failed browser test (saved to test-results/).
"""
import pytest

from data.config import (
    ACADEMY_1_BASE_URL,
    ACADEMY_1_PASSWORD,
    ACADEMY_1_USERNAME,
    EVALYTICS_AUTOMATION_ENABLED,
)


def pytest_collection_modifyitems(config, items):
    """Skip mutating tests unless the automation gate is enabled."""
    if EVALYTICS_AUTOMATION_ENABLED:
        return
    skip_mutating = pytest.mark.skip(
        reason=(
            "Mutating test — set EVALYTICS_AUTOMATION_ENABLED=true "
            "against a disposable environment to run it"
        )
    )
    for item in items:
        if "mutating" in item.keywords:
            item.add_marker(skip_mutating)


@pytest.fixture(scope="session")
def target_base_url():
    """Base URL of the application under test."""
    from data.config import BASE_URL
    return BASE_URL


@pytest.fixture(scope="session")
def academy_1_credentials():
    """Approved academy test account, or skip with instructions."""
    if not (ACADEMY_1_BASE_URL and ACADEMY_1_USERNAME and ACADEMY_1_PASSWORD):
        pytest.skip(
            "Approved academy account not configured — set "
            "ACADEMY_1_BASE_URL / ACADEMY_1_USERNAME / ACADEMY_1_PASSWORD "
            "in .env (locally) or as repository secrets (CI)"
        )
    return {
        "base_url": ACADEMY_1_BASE_URL,
        "username": ACADEMY_1_USERNAME,
        "password": ACADEMY_1_PASSWORD,
    }
