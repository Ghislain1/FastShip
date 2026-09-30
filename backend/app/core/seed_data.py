"""Dev-only mock data.

Enabled with `MOCK_SEED=true`. Inserts fake shipments and their orders so the
frontend has something to render. Never enable this in a deployed environment.

The data is deterministic on purpose: re-running with an empty database
produces the same rows, so screenshots and tests stay stable.
"""

from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order
from ..models.shipment import Shipment, ShipmentStatus
from ..repositories.order_repository import OrderRepository
from ..repositories.shipment_repository import ShipmentRepository
from .utils import get_datetime_utc

# Every documented lifecycle stage appears at least once, so the seeded data
# exercises the whole enum.
# (status, weight_kg, destination, tracking_number, [order quantities])
MOCK_SHIPMENTS: tuple[tuple[ShipmentStatus, float, str, str, tuple[int, ...]], ...] = (
    (ShipmentStatus.PENDING, 1.2, "Hamburg, DE", "FS1000000001", (1,)),
    (ShipmentStatus.PROCESSING, 0.4, "Munich, DE", "FS1000000002", (2, 1)),
    (ShipmentStatus.SHIPPED, 3.8, "Berlin, DE", "FS1000000003", (1,)),
    (ShipmentStatus.IN_TRANSIT, 0.9, "Cologne, DE", "FS1000000004", (3,)),
    (ShipmentStatus.OUT_FOR_DELIVERY, 2.5, "Vienna, AT", "FS1000000005", (1,)),
    (ShipmentStatus.DELIVERED, 0.7, "Zurich, CH", "FS1000000006", (2,)),
    (ShipmentStatus.FAILED, 5.1, "Paris, FR", "FS1000000007", (1,)),
    (ShipmentStatus.RETURNED, 1.6, "Amsterdam, NL", "FS1000000008", (4, 1)),
)


async def seed_mock_shipments(session: AsyncSession) -> int:
    """Insert mock shipments and orders. Idempotent.

    Returns the number of shipments inserted; 0 if any shipment already exists,
    so calling this on every startup is safe.
    """
    shipment_repository = ShipmentRepository(session)
    order_repository = OrderRepository(session)

    if await shipment_repository.count() > 0:
        return 0

    now = get_datetime_utc()

    for index, (status, weight, destination, tracking, quantities) in enumerate(
        MOCK_SHIPMENTS
    ):
        shipment = await shipment_repository.add(
            Shipment(
                status=status,
                weight=weight,
                destination=destination,
                tracking_number=tracking,
            )
        )

        # Older rows get older timestamps so the data reads like a history.
        placed_at = now - timedelta(hours=len(MOCK_SHIPMENTS) - index)

        for quantity in quantities:
            await order_repository.add(
                Order(
                    quantity=quantity,
                    shipment_id=shipment.id,
                    created_at=placed_at,
                    updated_at=placed_at,
                )
            )

    return len(MOCK_SHIPMENTS)
