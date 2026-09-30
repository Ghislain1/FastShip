from uuid import UUID

from fastapi.exceptions import HTTPException
from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.shipment import Shipment, ShipmentStatus
from ..repositories.order_repository import OrderRepository
from ..repositories.shipment_repository import ShipmentRepository
from ..schemas.shipment import ShipmentCreate, ShipmentUpdate


class ShipmentService:
    """Business rules for shipments. All queries live in the repositories."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ShipmentRepository(session)
        self.order_repository = OrderRepository(session)

    async def create_shipment(self, shipment_create: ShipmentCreate) -> Shipment:
        shipment = Shipment.model_validate(shipment_create)
        return await self.repository.add(shipment)

    async def load_shipments(
        self,
        offset: int,
        limit: int,
        *,
        status_filter: ShipmentStatus | None = None,
        destination: str | None = None,
        sort_by: str = "tracking_number",
        descending: bool = False,
    ) -> list[Shipment]:
        return await self.repository.list(
            offset,
            limit,
            status=status_filter,
            destination=destination,
            sort_by=sort_by,
            descending=descending,
        )

    async def count_shipments(
        self,
        *,
        status_filter: ShipmentStatus | None = None,
        destination: str | None = None,
    ) -> int:
        """Total matching the same filters as `load_shipments`."""
        return await self.repository.count(
            status=status_filter, destination=destination
        )

    async def get_shipment_by_id(self, id: UUID) -> Shipment:
        shipment = await self.repository.get_by_id(id)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
            )
        return shipment

    async def update_shipment(
        self, id: UUID, shipment_update: ShipmentUpdate
    ) -> Shipment:
        """PATCH semantics: only the fields that were set are changed."""
        shipment = await self.get_shipment_by_id(id)

        changes = shipment_update.model_dump(exclude_unset=True, exclude_none=True)
        if not changes:
            return shipment

        for field, value in changes.items():
            setattr(shipment, field, value)

        return await self.repository.update(shipment)

    async def delete_shipment(self, id: UUID) -> int:
        """Delete a shipment and every order attached to it.

        Returns the number of orders that were removed with it.
        """
        shipment = await self.get_shipment_by_id(id)

        removed_orders = await self.order_repository.delete_by_shipment_id(shipment.id)
        await self.repository.delete(shipment)

        return removed_orders
