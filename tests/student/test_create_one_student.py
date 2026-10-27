"""
Create one student through the Evalytics public join flow.
"""

import pytest

from pages.auth.login import LoginPage
from pages.academy.academy_settings_page import (
    AcademySettingsPage,
)
from pages.student.student_registration_page import (
    StudentRegistrationPage,
)

from utils.save_student_data import (
    save_student_data,
)

pytestmark = [pytest.mark.mutating, pytest.mark.accounts]


def test_create_one_student(page, browser, academy_1_credentials, target_base_url):

    # --------------------------------------------------------
    # Step 1: Login as academy teacher
    # --------------------------------------------------------

    login_page = LoginPage(page)

    login_page.open(
        academy_1_credentials["base_url"]
    )

    login_page.login(
        academy_1_credentials["username"],
        academy_1_credentials["password"],
    )

    assert login_page.is_logged_in(), (
        "Academy login failed"
    )

    # --------------------------------------------------------
    # Step 2: Open Academy Settings
    # --------------------------------------------------------

    academy_settings_page = AcademySettingsPage(page)

    academy_settings_page.open(
        academy_1_credentials["base_url"]
    )

    # --------------------------------------------------------
    # Step 3: Retrieve Join Code
    # --------------------------------------------------------

    join_code = (
        academy_settings_page.get_join_code()
    )

    assert join_code, (
        "Join Code was not found"
    )

    print(
        "\nJoin Code retrieved successfully"
    )

    # --------------------------------------------------------
    # Step 4: Create a fresh browser context
    # --------------------------------------------------------
    # This keeps the student session separate from
    # the teacher session.

    student_context = browser.new_context()

    student_browser_page = (
        student_context.new_page()
    )

    student_page = StudentRegistrationPage(
        student_browser_page
    )

    # --------------------------------------------------------
    # Step 5: Open student registration page
    # --------------------------------------------------------

    student_page.open(
        target_base_url,
        join_code,
    )

    print(
        "\nStudent registration URL:"
    )
    print(
        student_browser_page.url
    )

    print(
        "\nPage title:"
    )
    print(
        student_browser_page.title()
    )

    # --------------------------------------------------------
    # Step 6: Student test data
    # --------------------------------------------------------

    student_name = (
        "Evalytics Test Student"
    )

    student_email = (
        "evalytics.test.student@example.com"
    )

    student_password = (
        "TestStudent123"
    )

    preferred_language = "en"

    # --------------------------------------------------------
    # Step 7: Register student
    # --------------------------------------------------------

    student_page.register(
        name=student_name,
        email=student_email,
        password=student_password,
        preferred_language=preferred_language,
    )

    print(
        "\nStudent registration submitted"
    )

    # --------------------------------------------------------
    # Step 8: Save student details
    # --------------------------------------------------------

    save_student_data(
        {
            "name": student_name,
            "email": student_email,
            "password": student_password,
            "preferred_language": preferred_language,
            "academy_base_url": academy_1_credentials["base_url"],
        }
    )

    print(
        "Student details saved successfully"
    )

    # --------------------------------------------------------
    # Step 9: Close student browser context
    # --------------------------------------------------------

    student_context.close()