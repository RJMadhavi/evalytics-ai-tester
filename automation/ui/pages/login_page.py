import re

from .base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    @property
    def email(self):
        return self.page.locator("input[type='email'], input[name='email']").first

    @property
    def password(self):
        return self.page.locator("input[type='password']").first

    @property
    def sign_in(self):
        return self.page.get_by_role("button", name=re.compile("sign in", re.I))
