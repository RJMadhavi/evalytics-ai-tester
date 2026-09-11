"""
Evalytics Academy Settings Page
"""

from playwright.sync_api import Page


class AcademySettingsPage:

    def __init__(self, page: Page):
        self.page = page

        self.join_code = page.locator(
            "#join-code-text"
        )

    def open(self, base_url: str):
        self.page.goto(
            f"{base_url}/teacher/academy-settings"
        )

    def get_join_code(self) -> str:
        return self.join_code.inner_text().strip().replace("-", "")