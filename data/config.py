import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Target Application
# ============================================================
# The application under test. Point this at a disposable
# environment whenever possible. Production (evalytics.in)
# may only be used for READ-ONLY smoke tests.
BASE_URL = os.getenv("BASE_URL", "https://evalytics.in")

CREATE_ACADEMY_PATH = os.getenv(
    "CREATE_ACADEMY_PATH", "/create-academy"
)

# Query parameters the /create-academy page expects
# (plan/billing selection from the pricing page).
CREATE_ACADEMY_PARAMS = {
    "billing": os.getenv("CREATE_ACADEMY_BILLING", "monthly"),
    "teachers": os.getenv("CREATE_ACADEMY_TEACHERS", "1"),
    "students": os.getenv("CREATE_ACADEMY_STUDENTS", "10"),
}

# ============================================================
# Safety gate for tests that CREATE data
# ============================================================
# Tests marked @pytest.mark.mutating create academies,
# students, or exams. They are skipped unless this flag is
# explicitly "true", and should only target a disposable
# environment — never production.
EVALYTICS_AUTOMATION_ENABLED = os.getenv(
    "EVALYTICS_AUTOMATION_ENABLED", "false"
).lower() == "true"


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
