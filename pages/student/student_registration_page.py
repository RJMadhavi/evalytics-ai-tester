"""
Evalytics Student Registration Page
"""

from playwright.sync_api import Page


class StudentRegistrationPage:

    def __init__(self, page: Page):
        self.page = page

        # Registration form
        self.name = page.locator("#name")

        self.email = page.locator("#email")

        self.preferred_language = page.locator(
            "select[name='preferred_language']"
        )

        self.password = page.locator("#password")

        self.confirm_password = page.locator(
            "#confirm_password"
        )

        self.submit_button = page.locator(
            "#submit-btn"
        )

    def open(self, base_url: str, join_code: str):
        self.page.goto(
            f"{base_url}/join/{join_code}"
        )

    def register(
        self,
        name: str,
        email: str,
        password: str,
        preferred_language: str = "en",
    ):
        self.name.fill(name)

        self.email.fill(email)

        self.preferred_language.select_option(
            preferred_language
        )

        self.password.fill(password)

        self.confirm_password.fill(password)

        self.submit_button.click()