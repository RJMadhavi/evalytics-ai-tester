from data.config import (
    ACADEMY_1_BASE_URL,
    ACADEMY_1_USERNAME,
    ACADEMY_1_PASSWORD,
)

from pages.auth.login import LoginPage
from pages.academy.academy_settings_page import (
    AcademySettingsPage,
)


def test_get_academy_join_code(page):
    # Create our Page Object instances.
    login_page = LoginPage(page)

    # Step 1: Open the academy.
    login_page.open(ACADEMY_1_BASE_URL)

    # Step 2: Log in using Academy 1 credentials.
    login_page.login(
        ACADEMY_1_USERNAME,
        ACADEMY_1_PASSWORD,
    )

    # Verify login was successful.
    assert login_page.is_logged_in(), (
        "Academy login failed"
    )

    # Step 3: Open Academy Settings.
    academy_settings_page = AcademySettingsPage(page)

    academy_settings_page.open(
        ACADEMY_1_BASE_URL
    )

    # Step 4: Get the Join Code.
    join_code = academy_settings_page.get_join_code()

    # Step 5: Verify that a Join Code was found.
    assert join_code, (
        "Join Code was not found"
    )

    # Do not print the actual Join Code.
    print("\nAcademy Settings opened")
    print("Join Code successfully retrieved")
    print(
        f"Join Code length: {len(join_code)} characters"
    )