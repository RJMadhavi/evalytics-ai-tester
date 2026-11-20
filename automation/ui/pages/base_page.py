import re

VERSION_RE = re.compile(r"\bv(\d+\.\d+\.\d+)\b")


class BasePage:
    path = "/"

    def __init__(self, page):
        self.page = page

    def open(self):
        return self.page.goto(self.path)

    def title(self):
        return self.page.title()

    def footer_version(self):
        """The version string shown in the footer, such as 1.1.0, or None."""
        match = VERSION_RE.search(self.page.locator("body").inner_text())
        return match.group(1) if match else None
