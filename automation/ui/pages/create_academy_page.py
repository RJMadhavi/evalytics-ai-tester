import re

from .base_page import BasePage

# From the live form (page text read on 2026-11-16). Check with tools/dump_form.py.
SUBJECTS = (
    "Chemistry", "Physics", "Mathematics", "Biology", "English",
    "History", "Geography", "Economics", "Computer Science", "Other",
)


class CreateAcademyPage(BasePage):
    path = "/create-academy"

    # Locators use the visible label text, as a user (and a screen reader) would.
    # If one fails to resolve, the field probably has no accessible label: that is a finding.
    @property
    def academy_name(self):
        return self.page.get_by_label(re.compile(r"Academy\s*/\s*Institute Name", re.I))

    @property
    def subdomain(self):
        return self.page.get_by_label(re.compile(r"Choose Your Subdomain", re.I))

    @property
    def full_name(self):
        return self.page.get_by_label(re.compile(r"Your Full Name", re.I))

    @property
    def subject(self):
        return self.page.get_by_label(re.compile(r"Subject You Teach", re.I))

    @property
    def email(self):
        return self.page.get_by_label(re.compile(r"^\s*Email Address", re.I))

    @property
    def password(self):
        return self.page.get_by_label("Password", exact=True)

    @property
    def confirm_password(self):
        return self.page.get_by_label(re.compile(r"Confirm Password", re.I))

    @property
    def preview(self):
        """The live line under the subdomain box, such as 'yourname.evalytics.in'."""
        return self.page.get_by_text(re.compile("🌐"))

    @property
    def terms_link(self):
        return self.page.get_by_role("link", name=re.compile("Terms of Service", re.I))

    @property
    def privacy_link(self):
        return self.page.get_by_role("link", name=re.compile("Privacy Policy", re.I))

    @property
    def submit_button(self):
        return self.page.get_by_role("button", name=re.compile(r"Create Academy", re.I))

    def fill(self, name, subdomain, full_name, email, password, confirm):
        """Type into the form. Does not submit."""
        self.academy_name.fill(name)
        self.subdomain.fill(subdomain)
        self.full_name.fill(full_name)
        self.email.fill(email)
        self.password.fill(password)
        self.confirm_password.fill(confirm)
