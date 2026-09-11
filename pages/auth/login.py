"""
Evalytics Login Page
"""

from playwright.sync_api import Page


class LoginPage:

    def __init__(self, page: Page):
        self.page = page

        # Login form
        self.username = page.locator("#email")

        self.password = page.locator("#password")

        self.login_button = page.get_by_role(
            "button",
            name="Sign In",
        )

    def open(self, base_url: str):
        self.page.goto(base_url)

    def login(
        self,
        username: str,
        password: str,
    ):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def is_logged_in(self) -> bool:
        return "login" not in self.page.url.lower()