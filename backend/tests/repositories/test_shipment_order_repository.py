from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import get_datetime_utc
from app.models.order import Order
from app.models.shipment import Shipment, ShipmentStatus
from app.repositories.order_repository import OrderRepository
from app.repositories.shipment_repository import ShipmentRepository
from tests.utils.utils import random_lower_string


def _shipment(**overrides) -> Shipment:
    defaults = {
        "status": ShipmentStatus.PENDING,
        "weight": 1.0,
        "destination": random_lower_string(),
        "tracking_number": random_lower_string(),
    }
    return Shipment(**{**defaults, **overrides})


async def test_shipment_list_is_paginated(db: AsyncSession) -> None:
    repository = ShipmentRepository(db)
    for _ in range(3):
        await repository.add(_shipment())

    assert len(await repository.list(offset=0, limit=2)) == 2
    assert len(await repository.list(offset=2, limit=10)) == 1
    assert await repository.get_by_id(uuid4()) is None


async def test_shipment_list_filters_and_sorts(db: AsyncSession) -> None:
    repository = ShipmentRepository(db)
    await repository.add(
        _shipment(status=ShipmentStatus.PENDING, destination="Berlin, DE")
    )
    await repository.add(
        _shipment(status=ShipmentStatus.DELIVERED, destination="Berlin, DE")
    )
    await repository.add(
        _shipment(status=ShipmentStatus.DELIVERED, destination="Paris, FR")
    )

    delivered = await repository.list(
        0, 10, status=ShipmentStatus.DELIVERED, sort_by="destination"
    )
    assert [s.destination for s in delivered] == ["Berlin, DE", "Paris, FR"]

    descending = await repository.list(0, 10, sort_by="destination", descending=True)
    assert [s.destination for s in descending] == [
        "Paris, FR",
        "Berlin, DE",
        "Berlin, DE",
    ]

    assert await repository.count(status=ShipmentStatus.DELIVERED) == 2
    assert await repository.count(destination="Berlin, DE") == 2
    assert await repository.count() == 3


async def test_order_list_returns_rows(db: AsyncSession) -> None:
    order_repository = OrderRepository(db)
    shipment = await ShipmentRepository(db).add(_shipment())
    assert await order_repository.list() == []

    await order_repository.add(
        Order(
            quantity=1,
            shipment_id=shipment.id,
            created_at=get_datetime_utc(),
            updated_at=get_datetime_utc(),
        )
    )

    orders = await order_repository.list()
    assert len(orders) == 1
    assert orders[0].quantity == 1
    assert orders[0].shipment_id == shipment.id


async def test_delete_by_shipment_id_removes_only_its_orders(db: AsyncSession) -> None:
    shipment_repository = ShipmentRepository(db)
    order_repository = OrderRepository(db)

    keep = await shipment_repository.add(_shipment())
    drop = await shipment_repository.add(_shipment())

    for shipment, quantity in ((keep, 1), (drop, 2), (drop, 3)):
        await order_repository.add(
            Order(
                quantity=quantity,
                shipment_id=shipment.id,
                created_at=get_datetime_utc(),
                updated_at=get_datetime_utc(),
            )
        )

    assert await order_repository.delete_by_shipment_id(drop.id) == 2

    remaining = await order_repository.list()
    assert len(remaining) == 1
    assert remaining[0].shipment_id == keep.id
