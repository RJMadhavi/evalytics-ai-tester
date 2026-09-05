'''
        Using this file to generate the test data by creating tenants.
'''

from faker import Faker


class TenantDataFactory:
    """Generates realistic test data for an Evalytics tenant."""

    def __init__(self, seed=None):
        self.fake = Faker()

        if seed is not None:
            self.fake.seed_instance(seed)

    def create(self, index: int):
        unique_id = self.fake.unique.random_int(
            min=1000,
            max=999999
        )

        academy_name = f"{self.fake.company()} Academy {index}"

        subdomain = (
            f"automation-{index}-{unique_id}"
            .lower()
            .replace(" ", "-")
        )

        return {
            "academy_name": academy_name,
            "subdomain": subdomain,
            "admin_first_name": self.fake.first_name(),
            "admin_last_name": self.fake.last_name(),
            "email": f"automation.tenant{index}.{unique_id}@example.com",
            "password": self.fake.password(
                length=16,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        }