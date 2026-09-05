'''
        This test verifies the the generator.
'''
from data.factories.tenant_data import TenantDataFactory


def test_generate_two_tenants():
    factory = TenantDataFactory(seed=12345)

    tenant1 = factory.create(1)
    tenant2 = factory.create(2)

    assert tenant1["academy_name"]
    assert tenant2["academy_name"]

    assert tenant1["email"] != tenant2["email"]
    assert tenant1["subdomain"] != tenant2["subdomain"]

    print("\nTenant 1:")
    print(tenant1)

    print("\nTenant 2:")
    print(tenant2)
