import os
from dotenv import load_dotenv

load_dotenv()

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


# ============================================================
# Approved Academy Accounts
# ============================================================

ACADEMY_1_BASE_URL = os.getenv(
    "ACADEMY_1_BASE_URL",
    ""
)

ACADEMY_1_USERNAME = os.getenv(
    "ACADEMY_1_USERNAME",
    ""
)

ACADEMY_1_PASSWORD = os.getenv(
    "ACADEMY_1_PASSWORD",
    ""
)


ACADEMY_2_BASE_URL = os.getenv(
    "ACADEMY_2_BASE_URL",
    ""
)

ACADEMY_2_USERNAME = os.getenv(
    "ACADEMY_2_USERNAME",
    ""
)

ACADEMY_2_PASSWORD = os.getenv(
    "ACADEMY_2_PASSWORD",
    ""
)