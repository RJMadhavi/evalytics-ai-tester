import json
from datetime import datetime
from pathlib import Path

from data.config import CREATE_ACADEMY_PARAMS


REPORT_DIR = Path("reports")
REPORT_FILE = REPORT_DIR / "academy_creation_report.json"


def save_tenant_report(
    tenants: list[dict],
    subjects: list[str],
    selected_subjects: list[str],
    status: str = "PASS",
):
    """
    Save the complete academy creation test data for one
    test execution.
    """

    REPORT_DIR.mkdir(exist_ok=True)

    tenant_records = []

    for tenant, selected_subject in zip(
        tenants,
        selected_subjects,
    ):
        tenant_records.append(
            {
                "tenant_number": tenant["tenant_number"],
                "academy_name": tenant["academy_name"],
                "subdomain": tenant["subdomain"],
                "admin_first_name": tenant["admin_first_name"],
                "admin_last_name": tenant["admin_last_name"],
                "email": tenant["email"],
                "password": tenant["password"],
                "subject": selected_subject,
            }
        )

    report = {
        "generated_at": datetime.now().astimezone().isoformat(),
        "status": status,
        "academy_configuration": {
            **CREATE_ACADEMY_PARAMS,
            "available_subjects": subjects,
        },
        "tenants": tenant_records,
    }

    with REPORT_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=4,
        )

    return REPORT_FILE
