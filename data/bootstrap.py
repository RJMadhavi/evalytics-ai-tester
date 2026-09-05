from data.config import (
    TENANT_COUNT,
    STUDENTS_PER_TENANT,
    TEACHERS_PER_TENANT,
    REVIEWERS_PER_TENANT,
    AUTOMATION_PREFIX,
)


def main():
    print("========================================")
    print(" Evalytics Test Data Bootstrap")
    print("========================================")
    print(f"Automation prefix:   {AUTOMATION_PREFIX}")
    print(f"Tenants:             {TENANT_COUNT}")
    print(f"Teachers / tenant:   {TEACHERS_PER_TENANT}")
    print(f"Reviewers / tenant:  {REVIEWERS_PER_TENANT}")
    print(f"Students / tenant:   {STUDENTS_PER_TENANT}")
    print()
    print("Bootstrap configuration loaded successfully.")


if __name__ == "__main__":
    main()