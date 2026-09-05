import os


# ============================================================
# Evalytics Test Data Configuration
# ============================================================

TENANT_COUNT = int(os.getenv("TENANT_COUNT", "2"))

STUDENTS_PER_TENANT = int(
    os.getenv("STUDENTS_PER_TENANT", "10")
)

TEACHERS_PER_TENANT = int(
    os.getenv("TEACHERS_PER_TENANT", "1")
)

REVIEWERS_PER_TENANT = int(
    os.getenv("REVIEWERS_PER_TENANT", "1")
)


# Prefix used to identify records created by automation.
AUTOMATION_PREFIX = os.getenv(
    "AUTOMATION_PREFIX",
    "Evalytics Automation"
)