'''
    A Test to create an academy.
'''

from urllib.parse import urlencode

from playwright.sync_api import Page

from data.config import (
    BASE_URL,
    CREATE_ACADEMY_PATH,
    CREATE_ACADEMY_PARAMS,
)


class CreateAcademyPage:

    def __init__(self, page: Page):
        self.page = page

        self.academy_name = page.get_by_role(
            "textbox",
            name="e.g. Shrinath Chemistry"
        )

        self.subdomain = page.get_by_role(
            "textbox",
            name="shrinathchemistry"
        )

        self.full_name = page.get_by_role(
            "textbox",
            name="e.g. Rajesh Kumar"
        )

        self.subject = page.get_by_role(
            "combobox"
        )

        self.email = page.get_by_role(
            "textbox",
            name="you@example.com"
        )

        self.password = page.get_by_role(
            "textbox",
            name="Min. 8 characters"
        )

        self.confirm_password = page.get_by_role(
            "textbox",
            name="Repeat password"
        )

        self.create_academy = page.get_by_role(
            "button",
            name="Create Academy"
        )

    def open(self):
        """
        Open the Create Academy page with the configured
        plan and billing parameters.
        """
        query_string = urlencode(CREATE_ACADEMY_PARAMS)

        url = (
            f"{BASE_URL}"
            f"{CREATE_ACADEMY_PATH}"
            f"?{query_string}"
        )

        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    def get_subject_options(self):
        """
        Return all selectable subjects from the Subject
        dropdown.

        The placeholder option is excluded and whitespace
        is cleaned from the option text.
        """
        options = self.subject.locator(
            "option"
        ).all_text_contents()

        subjects = [
            option.strip()
            for option in options
            if option.strip()
            and option.strip() != "— Select subject —"
        ]

        return subjects

    def select_subject_for_tenant(
        self,
        subjects: list[str],
        tenant_number: int,
    ) -> str:
        """
        Select a subject deterministically based on the
        tenant number.

        Tenant 1 -> first subject
        Tenant 2 -> second subject
        Tenant 3 -> third subject

        If there are more tenants than subjects, the
        selection cycles back to the beginning.
        """
        if not subjects:
            raise AssertionError(
                "No selectable subjects were found"
            )

        subject_index = (
            tenant_number - 1
        ) % len(subjects)

        selected_subject = subjects[subject_index]

        self.subject.select_option(
            label=selected_subject
        )

        return selected_subject

    def fill_academy_details(self, tenant: dict):
        """
        Fill academy-level information.
        """
        self.academy_name.fill(
            tenant["academy_name"]
        )

        self.subdomain.fill(
            tenant["subdomain"]
        )

    def fill_teacher_account(self, tenant: dict):
        """
        Fill administrator/teacher account information.
        """
        self.full_name.fill(
            f'{tenant["admin_first_name"]} '
            f'{tenant["admin_last_name"]}'
        )

        self.email.fill(
            tenant["email"]
        )

        self.password.fill(
            tenant["password"]
        )

        self.confirm_password.fill(
            tenant["password"]
        )