"""
Test Create Academy Page

This test:
1. Generates tenant data.
2. Discovers available subjects from the application.
3. Populates the Create Academy form.
4. Validates all populated fields.
5. Submits the academy registration.
6. Verifies the Registration Received confirmation.
7. Records the result in the test report.
"""

from data.config import TENANT_COUNT
from data.factories.tenant_data import TenantDataFactory
from data.reporting import save_tenant_report
from pages.academy.create_academy_page import CreateAcademyPage


def test_create_academy_form_with_generated_data(page):
    factory = TenantDataFactory(seed=12345)

    tenants = []

    for tenant_number in range(1, TENANT_COUNT + 1):
        tenant = factory.create(tenant_number)
        tenant["tenant_number"] = tenant_number
        tenants.append(tenant)

    academy_page = CreateAcademyPage(page)

    academy_page.open()

    # ---------------------------------------------------------
    # Discover subjects from the application
    # ---------------------------------------------------------

    subjects = academy_page.get_subject_options()

    print(
        f"\nAvailable subjects: {subjects}"
    )

    assert subjects, (
        "No subjects were found in the Subject dropdown"
    )

    # ---------------------------------------------------------
    # Tenant 2
    #
    # Tenant 1 has already been submitted successfully.
    # We therefore submit Tenant 2 in this run.
    # ---------------------------------------------------------

    tenant = tenants[1]

    tenant_number = tenant["tenant_number"]

    academy_page.fill_academy_details(tenant)

    selected_subject = (
        academy_page.select_subject_for_tenant(
            subjects=subjects,
            tenant_number=tenant_number,
        )
    )

    print(
        f"Tenant {tenant_number}: "
        f"{tenant['academy_name']}"
    )

    print(
        f"Tenant {tenant_number} subject: "
        f"{selected_subject}"
    )

    academy_page.fill_teacher_account(tenant)

    # ---------------------------------------------------------
    # Validate populated form
    # ---------------------------------------------------------

    assert academy_page.academy_name.input_value() == (
        tenant["academy_name"]
    )

    assert academy_page.subdomain.input_value() == (
        tenant["subdomain"]
    )

    assert academy_page.full_name.input_value() == (
        f'{tenant["admin_first_name"]} '
        f'{tenant["admin_last_name"]}'
    )

    assert academy_page.email.input_value() == (
        tenant["email"]
    )

    assert academy_page.password.input_value() == (
        tenant["password"]
    )

    assert academy_page.confirm_password.input_value() == (
        tenant["password"]
    )

    assert academy_page.subject.input_value() == (
        selected_subject
    )

    assert academy_page.create_academy.is_visible()

    print(
        f"Tenant {tenant_number} form validation: PASS"
    )

    # ---------------------------------------------------------
    # Submit academy registration
    # ---------------------------------------------------------

    academy_page.create_academy.click()

    academy_page.page.wait_for_load_state(
        "domcontentloaded"
    )

    print(
        f"After Create Academy click:"
        f"\n  URL: {academy_page.page.url}"
        f"\n  Title: {academy_page.page.title()}"
    )

    # ---------------------------------------------------------
    # Verify Registration Received page
    # ---------------------------------------------------------

    assert academy_page.page.get_by_text(
        "Registration Received!",
        exact=True,
    ).is_visible()

    assert academy_page.page.get_by_text(
        tenant["academy_name"],
        exact=True,
    ).is_visible()

    assert academy_page.page.get_by_text(
        "has been registered and is awaiting approval.",
        exact=False,
    ).is_visible()

    assert academy_page.page.get_by_text(
        "You'll receive a confirmation email",
        exact=False,
    ).is_visible()

    print(
        f"Tenant {tenant_number} registration: PASS"
    )

    # ---------------------------------------------------------
    # Save report
    # ---------------------------------------------------------

    save_tenant_report(
        tenants=[tenant],
        subjects=subjects,
        selected_subjects=[selected_subject],
        status="PASS",
    )