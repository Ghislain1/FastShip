"""Phase 1 auth contract: tokens are validated, and no endpoint leaks data."""

from uuid import uuid4

import pytest

from app.core.utils import generate_access_token
from tests.utils.utils import auth_headers, random_email

PROTECTED_ENDPOINTS = [
    "/sellers/",
    "/shipments",
    "/order/",
    "/order/user/order/1/",
]


def _create_seller(test_client, payload) -> str:
    response = test_client.post("/auth/signup", json=payload)
    assert response.status_code == 200, response.text
    return response.json()["email"]


@pytest.mark.parametrize("path", PROTECTED_ENDPOINTS)
def test_endpoints_require_a_token(test_client, registered_seller, path):
    assert test_client.get(path).status_code == 401


@pytest.mark.parametrize("path", PROTECTED_ENDPOINTS)
def test_invalid_token_is_rejected(test_client, registered_seller, path):
    response = test_client.get(path, headers={"Authorization": "Bearer garbage"})
    assert response.status_code == 401


def test_sellers_requires_a_valid_token(test_client, registered_seller):
    headers = auth_headers(registered_seller["email"])
    response = test_client.get("/sellers/", headers=headers)
    assert response.status_code == 200
    assert response.json()["count"] == 1


def test_shipments_accepts_a_valid_token(test_client, registered_seller):
    headers = auth_headers(registered_seller["email"])
    assert test_client.get("/shipments", headers=headers).status_code == 200


def test_token_signed_with_another_key_is_rejected(test_client, registered_seller):
    import jwt

    forged = jwt.encode(
        {
            "user": {
                "email": registered_seller["email"],
                "name": "x",
                "id": str(uuid4()),
            }
        },
        key="attacker-key",
        algorithm="HS256",
    )
    response = test_client.get(
        "/sellers/", headers={"Authorization": f"Bearer {forged}"}
    )
    assert response.status_code == 401


def test_token_for_unknown_seller_is_rejected(test_client, registered_seller):
    response = test_client.get("/sellers/", headers=auth_headers(random_email()))
    assert response.status_code == 401


def test_token_payload_without_user_is_rejected(test_client, registered_seller):
    bare = generate_access_token({"nonsense": True})
    response = test_client.get("/sellers/", headers={"Authorization": f"Bearer {bare}"})
    assert response.status_code == 401


def test_order_route_does_not_echo_the_token(test_client, registered_seller):
    headers = auth_headers(registered_seller["email"])
    response = test_client.get("/order/user/order/1/", headers=headers)
    assert response.status_code == 200
    assert "eyJ" not in response.text
    assert headers["Authorization"].split(" ", 1)[1] not in response.text
