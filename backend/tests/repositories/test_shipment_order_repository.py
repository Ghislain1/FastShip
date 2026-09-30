from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import get_datetime_utc
from app.models.order import Order
from app.models.shipment import Shipment
from app.repositories.order_repository import OrderRepository
from app.repositories.shipment_repository import ShipmentRepository
from tests.utils.utils import random_lower_string


async def test_shipment_list_is_paginated(db: AsyncSession) -> None:
    repository = ShipmentRepository(db)
    for _ in range(3):
        await repository.add(
            Shipment(
                status=random_lower_string(),
                weight=1.0,
                destination=random_lower_string(),
                tracking_number=random_lower_string(),
            )
        )

    assert len(await repository.list(offset=0, limit=2)) == 2
    assert len(await repository.list(offset=2, limit=10)) == 1
    assert await repository.get_by_id(uuid4()) is None


async def test_order_list_returns_rows(db: AsyncSession) -> None:
    order_repository = OrderRepository(db)
    shipment = await ShipmentRepository(db).add(
        Shipment(
            status=random_lower_string(),
            weight=1.0,
            destination=random_lower_string(),
            tracking_number=random_lower_string(),
        )
    )
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
