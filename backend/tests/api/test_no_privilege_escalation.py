"""Phase 1: a client cannot grant itself privileges via the signup payload."""

from tests.utils.utils import auth_headers, random_email


def test_signup_cannot_set_is_superuser(test_client, seller_payload):
    response = test_client.post(
        "/auth/signup", json={**seller_payload, "is_superuser": True}
    )
    assert response.status_code == 200
    assert "is_superuser" not in response.json()


def test_escalated_seller_is_not_a_superuser(test_client, seller_payload):
    test_client.post("/auth/signup", json={**seller_payload, "is_superuser": True})

    # If the flag had been persisted, the seller would still be able to read
    # /sellers/ using their own token; assert the account works but carries no
    # privilege field anywhere in the public representation.
    response = test_client.get(
        "/sellers/", headers=auth_headers(seller_payload["email"])
    )
    assert response.status_code == 200
    for row in response.json()["data"]:
        assert "is_superuser" not in row


def test_signup_cannot_deactivate_itself(test_client, seller_payload):
    response = test_client.post(
        "/auth/signup", json={**seller_payload, "is_active": False}
    )
    assert response.status_code == 200
    assert response.json()["is_active"] is True


def test_duplicate_email_still_conflicts(test_client, registered_seller):
    response = test_client.post("/auth/signup", json=registered_seller)
    assert response.status_code == 409


def test_wrong_password_returns_401(test_client, registered_seller):
    response = test_client.post(
        "/auth/token",
        data={"username": registered_seller["email"], "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_unknown_email_and_wrong_password_are_indistinguishable(
    test_client, registered_seller
):
    """Guards against user enumeration: both failures must be byte-identical."""
    unknown = test_client.post(
        "/auth/token", data={"username": random_email(), "password": "wrong-password"}
    )
    wrong_password = test_client.post(
        "/auth/token",
        data={"username": registered_seller["email"], "password": "wrong-password"},
    )

    assert unknown.status_code == wrong_password.status_code == 401
    assert unknown.json() == wrong_password.json()


def test_login_returns_a_usable_token(test_client, registered_seller):
    response = test_client.post(
        "/auth/token",
        data={
            "username": registered_seller["email"],
            "password": registered_seller["password"],
        },
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    authorized = test_client.get(
        "/sellers/", headers={"Authorization": f"Bearer {token}"}
    )
    assert authorized.status_code == 200
