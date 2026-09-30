"""Full REST contract for /shipments."""

from datetime import UTC, datetime

import pytest

from app.models.shipment import ShipmentStatus
from app.schemas.shipment import ShipmentCreate
from tests.utils.utils import auth_headers, random_lower_string

MISSING_ID = "00000000-0000-0000-0000-000000000000"


def _payload(**overrides) -> dict:
    body = {
        "status": "pending",
        "weight": 2.5,
        "destination": "Berlin, DE",
        "tracking_number": "FS-0001",
    }
    return {**body, **overrides}


def _auth(registered_seller) -> dict:
    return auth_headers(registered_seller["email"])


# ---------------------------------------------------------------- create


def test_create_returns_201_and_the_resource(test_client, registered_seller):
    response = test_client.post(
        "/shipments", json=_payload(), headers=_auth(registered_seller)
    )

    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    assert body["weight"] == 2.5
    assert body["destination"] == "Berlin, DE"
    assert body["tracking_number"] == "FS-0001"
    assert body["id"]


def test_create_defaults_the_status(test_client, registered_seller):
    payload = _payload()
    payload.pop("status")

    response = test_client.post(
        "/shipments", json=payload, headers=_auth(registered_seller)
    )

    assert response.status_code == 201
    assert response.json()["status"] == "pending"


@pytest.mark.parametrize(
    "field,value",
    [
        ("status", "teleported"),
        ("weight", 0),
        ("weight", -3),
        ("destination", ""),
        ("tracking_number", ""),
    ],
)
def test_create_rejects_invalid_fields(test_client, registered_seller, field, value):
    response = test_client.post(
        "/shipments", json=_payload(**{field: value}), headers=_auth(registered_seller)
    )
    assert response.status_code == 422


def test_create_requires_auth(test_client):
    assert test_client.post("/shipments", json=_payload()).status_code == 401


# ------------------------------------------------------------------ read


def test_get_one_returns_the_shipment(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    response = test_client.get(f"/shipments/{created['id']}", headers=headers)

    assert response.status_code == 200
    assert response.json() == created


def test_get_one_unknown_id_is_404(test_client, registered_seller):
    response = test_client.get(
        f"/shipments/{MISSING_ID}", headers=_auth(registered_seller)
    )
    assert response.status_code == 404


def test_get_one_malformed_id_is_422(test_client, registered_seller):
    response = test_client.get(
        "/shipments/not-a-uuid", headers=_auth(registered_seller)
    )
    assert response.status_code == 422


def test_get_one_requires_auth(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    assert test_client.get(f"/shipments/{created['id']}").status_code == 401


# ------------------------------------------------------------------ list


def test_list_wraps_rows_and_count(test_client, registered_seller):
    headers = _auth(registered_seller)
    test_client.post("/shipments", json=_payload(), headers=headers)

    response = test_client.get("/shipments", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert len(body["data"]) == 1
    assert body["data"][0]["tracking_number"] == "FS-0001"


def test_list_paginates(test_client, registered_seller):
    headers = _auth(registered_seller)
    for index in range(5):
        test_client.post(
            "/shipments",
            json=_payload(tracking_number=f"FS-{index:04d}"),
            headers=headers,
        )

    page = test_client.get("/shipments/?offset=0&limit=2", headers=headers).json()
    assert page["count"] == 5
    assert len(page["data"]) == 2
    assert [row["tracking_number"] for row in page["data"]] == ["FS-0000", "FS-0001"]

    second = test_client.get("/shipments/?offset=2&limit=2", headers=headers).json()
    assert [row["tracking_number"] for row in second["data"]] == ["FS-0002", "FS-0003"]


@pytest.mark.parametrize("query", ["limit=0", "limit=101", "offset=-1"])
def test_list_rejects_out_of_range_pagination(test_client, registered_seller, query):
    response = test_client.get(f"/shipments/?{query}", headers=_auth(registered_seller))
    assert response.status_code == 422


def test_list_filters_by_status(test_client, registered_seller):
    headers = _auth(registered_seller)
    test_client.post(
        "/shipments",
        json=_payload(status="pending", tracking_number="A"),
        headers=headers,
    )
    test_client.post(
        "/shipments",
        json=_payload(status="delivered", tracking_number="B"),
        headers=headers,
    )

    response = test_client.get("/shipments/?status=delivered", headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["data"][0]["tracking_number"] == "B"


def test_list_rejects_unknown_status_filter(test_client, registered_seller):
    response = test_client.get(
        "/shipments/?status=teleported", headers=_auth(registered_seller)
    )
    assert response.status_code == 422


def test_list_filters_by_destination(test_client, registered_seller):
    headers = _auth(registered_seller)
    test_client.post(
        "/shipments", json=_payload(destination="Berlin, DE"), headers=headers
    )
    test_client.post(
        "/shipments", json=_payload(destination="Paris, FR"), headers=headers
    )

    response = test_client.get("/shipments/?destination=Paris, FR", headers=headers)

    assert response.json()["count"] == 1


def test_list_sorts_ascending_and_descending(test_client, registered_seller):
    headers = _auth(registered_seller)
    for tracking in ("C", "A", "B"):
        test_client.post(
            "/shipments", json=_payload(tracking_number=tracking), headers=headers
        )

    ascending = test_client.get("/shipments/?sort_by=tracking_number", headers=headers)
    descending = test_client.get(
        "/shipments/?sort_by=tracking_number&descending=true", headers=headers
    )

    assert [r["tracking_number"] for r in ascending.json()["data"]] == ["A", "B", "C"]
    assert [r["tracking_number"] for r in descending.json()["data"]] == ["C", "B", "A"]


def test_list_rejects_unknown_sort_field(test_client, registered_seller):
    response = test_client.get(
        "/shipments/?sort_by=hacked", headers=_auth(registered_seller)
    )
    assert response.status_code == 422


def test_list_requires_auth(test_client):
    assert test_client.get("/shipments").status_code == 401


def test_canonical_path_has_no_trailing_slash(test_client, registered_seller):
    headers = _auth(registered_seller)
    test_client.post("/shipments", json=_payload(), headers=headers)

    canonical = test_client.get("/shipments", headers=headers)
    assert canonical.status_code == 200

    # The legacy trailing-slash form still resolves, via a redirect.
    legacy = test_client.get("/shipments/", headers=headers, follow_redirects=True)
    assert legacy.status_code == 200
    assert legacy.json() == canonical.json()


# ---------------------------------------------------------------- update


def test_patch_changes_only_the_given_field(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    response = test_client.patch(
        f"/shipments/{created['id']}", json={"status": "shipped"}, headers=headers
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "shipped"
    assert body["weight"] == 2.5
    assert body["destination"] == "Berlin, DE"
    assert body["tracking_number"] == "FS-0001"


def test_patch_rejects_invalid_value(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    response = test_client.patch(
        f"/shipments/{created['id']}", json={"weight": -1}, headers=headers
    )
    assert response.status_code == 422


def test_patch_unknown_id_is_404(test_client, registered_seller):
    response = test_client.patch(
        f"/shipments/{MISSING_ID}",
        json={"status": "shipped"},
        headers=_auth(registered_seller),
    )
    assert response.status_code == 404


def test_patch_empty_body_is_a_noop(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    response = test_client.patch(
        f"/shipments/{created['id']}", json={}, headers=headers
    )

    assert response.status_code == 200
    assert response.json() == created


def test_put_replaces_the_resource(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    response = test_client.put(
        f"/shipments/{created['id']}",
        json=_payload(
            status="returned",
            weight=9.9,
            destination="Rome, IT",
            tracking_number="FS-9999",
        ),
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "returned"
    assert body["weight"] == 9.9
    assert body["destination"] == "Rome, IT"
    assert body["tracking_number"] == "FS-9999"


def test_put_requires_the_full_payload(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    response = test_client.put(
        f"/shipments/{created['id']}", json={"status": "shipped"}, headers=headers
    )
    assert response.status_code == 422


# ---------------------------------------------------------------- delete


def test_delete_returns_204_and_removes_it(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    response = test_client.delete(f"/shipments/{created['id']}", headers=headers)

    assert response.status_code == 204
    assert response.content == b""
    assert (
        test_client.get(f"/shipments/{created['id']}", headers=headers).status_code
        == 404
    )


def test_delete_unknown_id_is_404(test_client, registered_seller):
    response = test_client.delete(
        f"/shipments/{MISSING_ID}", headers=_auth(registered_seller)
    )
    assert response.status_code == 404


async def test_delete_cascades_to_orders(db):
    """A shipment's orders go with it, since order.shipment_id is NOT NULL.

    The HTTP response alone would not reveal orphaned order rows, so this
    asserts against the database directly.
    """
    from sqlalchemy import func, select

    from app.models.order import Order
    from app.models.shipment import Shipment
    from app.services.shipment_service import ShipmentService

    service = ShipmentService(db)
    target = await service.create_shipment(
        ShipmentCreate(
            status=ShipmentStatus.PENDING,
            weight=1.0,
            destination="Berlin, DE",
            tracking_number="FS-TARGET",
        )
    )
    survivor = await service.create_shipment(
        ShipmentCreate(
            status=ShipmentStatus.PENDING,
            weight=1.0,
            destination="Paris, FR",
            tracking_number="FS-SURVIVOR",
        )
    )

    now = datetime.now(UTC)
    # Two orders on the target, one on the survivor.
    for shipment_id in (target.id, target.id, survivor.id):
        db.add(
            Order(
                quantity=1,
                shipment_id=shipment_id,
                created_at=now,
                updated_at=now,
            )
        )
    await db.commit()

    async def order_count() -> int:
        result = await db.execute(select(func.count()).select_from(Order))
        return result.scalar_one()

    assert await order_count() == 3

    removed = await service.delete_shipment(target.id)

    assert removed == 2
    assert await order_count() == 1
    assert await db.get(Shipment, survivor.id) is not None
    assert await db.get(Shipment, target.id) is None

    remaining = (await db.execute(select(Order))).scalars().all()
    assert [o.shipment_id for o in remaining] == [survivor.id]


async def test_delete_shipment_without_orders_returns_zero(db):
    from app.services.shipment_service import ShipmentService

    service = ShipmentService(db)
    shipment = await service.create_shipment(
        ShipmentCreate(
            status=ShipmentStatus.PENDING,
            weight=1.0,
            destination="Nowhere, XX",
            tracking_number="FS-ALONE",
        )
    )

    assert await service.delete_shipment(shipment.id) == 0


async def test_delete_unknown_id_raises_404(db):
    from uuid import uuid4

    import pytest
    from fastapi import HTTPException

    from app.services.shipment_service import ShipmentService

    with pytest.raises(HTTPException) as exc:
        await ShipmentService(db).delete_shipment(uuid4())

    assert exc.value.status_code == 404


def test_delete_requires_auth(test_client, registered_seller):
    headers = _auth(registered_seller)
    created = test_client.post("/shipments", json=_payload(), headers=headers).json()

    assert test_client.delete(f"/shipments/{created['id']}").status_code == 401
    assert (
        test_client.get(f"/shipments/{created['id']}", headers=headers).status_code
        == 200
    )


def test_writes_are_not_shared_between_sellers(test_client, registered_seller):
    """Two sellers see the same shipments; there is no per-seller ownership yet."""
    from tests.utils.utils import random_email, random_password

    headers = _auth(registered_seller)
    other_email = random_email()
    other = test_client.post(
        "/auth/signup",
        json={"name": "Other", "email": other_email, "password": random_password()},
    )
    assert other.status_code == 200
    other_headers = auth_headers(other_email)

    test_client.post("/shipments", json=_payload(), headers=headers)

    assert test_client.get("/shipments", headers=other_headers).json()["count"] == 1


def test_tracking_numbers_need_not_be_unique(test_client, registered_seller):
    """No unique constraint is declared on tracking_number, so duplicates pass."""
    headers = _auth(registered_seller)
    payload = _payload(tracking_number=random_lower_string())

    first = test_client.post("/shipments", json=payload, headers=headers)
    second = test_client.post("/shipments", json=payload, headers=headers)

    assert first.status_code == second.status_code == 201
    assert first.json()["id"] != second.json()["id"]
