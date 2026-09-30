import pytest

from tests.utils.utils import random_email, random_lower_string, random_password


@pytest.fixture
def seller_payload() -> dict:
    return {
        "name": random_lower_string(),
        "email": random_email(),
        "password": random_password(),
    }


@pytest.fixture
def registered_seller(test_client, seller_payload) -> dict:
    """Register through the API so the row lands in the fixture database.

    We cannot rely on the lifespan-seeded superuser: the seeder writes to a
    different in-memory database than the `db` fixture session that
    `test_client` overrides `get_async_session` with.
    """
    response = test_client.post("/auth/signup", json=seller_payload)
    assert response.status_code == 200, response.text
    return seller_payload
