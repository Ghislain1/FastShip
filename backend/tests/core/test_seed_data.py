from sqlalchemy.ext.asyncio import AsyncSession

from app.core.seed_data import MOCK_SHIPMENTS, SHIPMENT_STATUSES, seed_mock_shipments
from app.models.shipment import Shipment
from app.repositories.order_repository import OrderRepository
from app.repositories.shipment_repository import ShipmentRepository


def _shipment(**overrides) -> Shipment:
    defaults = {
        "status": "delivered",
        "weight": 1.0,
        "destination": "Test, DE",
        "tracking_number": "TEST0001",
    }
    return Shipment(**{**defaults, **overrides})


async def test_seeds_every_shipment_and_its_orders(db: AsyncSession) -> None:
    inserted = await seed_mock_shipments(db)

    assert inserted == len(MOCK_SHIPMENTS)
    assert await ShipmentRepository(db).count() == len(MOCK_SHIPMENTS)

    expected_orders = sum(len(row[4]) for row in MOCK_SHIPMENTS)
    assert await OrderRepository(db).count() == expected_orders


async def test_is_idempotent(db: AsyncSession) -> None:
    first = await seed_mock_shipments(db)
    second = await seed_mock_shipments(db)

    assert first == len(MOCK_SHIPMENTS)
    assert second == 0
    assert await ShipmentRepository(db).count() == len(MOCK_SHIPMENTS)


async def test_skips_when_data_already_exists(db: AsyncSession) -> None:
    await ShipmentRepository(db).add(_shipment(tracking_number="EXISTING"))

    assert await seed_mock_shipments(db) == 0
    assert await ShipmentRepository(db).count() == 1


async def test_orders_reference_their_shipment(db: AsyncSession) -> None:
    await seed_mock_shipments(db)

    shipment_ids = {
        s.id for s in await ShipmentRepository(db).list(offset=0, limit=100)
    }

    orders = await OrderRepository(db).list()
    assert orders
    for order in orders:
        assert order.shipment_id in shipment_ids
        assert order.quantity >= 1
        assert order.created_at is not None
        assert order.updated_at is not None


async def test_statuses_cover_the_documented_lifecycle(db: AsyncSession) -> None:
    await seed_mock_shipments(db)

    seeded = {s.status for s in await ShipmentRepository(db).list(offset=0, limit=100)}
    assert seeded == set(SHIPMENT_STATUSES)


def test_mock_data_defines_no_unknown_status() -> None:
    for row in MOCK_SHIPMENTS:
        assert row[0] in SHIPMENT_STATUSES


def test_tracking_numbers_are_unique() -> None:
    tracking = [row[3] for row in MOCK_SHIPMENTS]
    assert len(tracking) == len(set(tracking))
