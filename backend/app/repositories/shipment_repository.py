from uuid import UUID

from sqlalchemy import Select, func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.shipment import Shipment, ShipmentStatus


class ShipmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Shipment | None:
        return await self.session.get(Shipment, id)

    def _apply_filters(
        self,
        statement: Select,
        *,
        status: ShipmentStatus | None = None,
        destination: str | None = None,
    ) -> Select:
        if status is not None:
            statement = statement.where(Shipment.status == status)
        if destination is not None:
            statement = statement.where(Shipment.destination == destination)
        return statement

    def _apply_sort(self, statement: Select, sort_by: str, descending: bool) -> Select:
        columns = {
            "tracking_number": Shipment.tracking_number,
            "destination": Shipment.destination,
            "weight": Shipment.weight,
            "status": Shipment.status,
        }
        column = columns.get(sort_by)
        if column is None:
            return statement
        return statement.order_by(column.desc() if descending else column.asc())

    async def list(
        self,
        offset: int,
        limit: int,
        *,
        status: ShipmentStatus | None = None,
        destination: str | None = None,
        sort_by: str = "tracking_number",
        descending: bool = False,
    ) -> list[Shipment]:
        statement = select(Shipment)
        statement = self._apply_filters(
            statement, status=status, destination=destination
        )
        statement = self._apply_sort(statement, sort_by, descending)
        statement = statement.offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def count(
        self,
        *,
        status: ShipmentStatus | None = None,
        destination: str | None = None,
    ) -> int:
        statement = select(func.count()).select_from(Shipment)
        statement = self._apply_filters(
            statement, status=status, destination=destination
        )
        return await self.session.scalar(statement)

    async def add(self, shipment: Shipment) -> Shipment:
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def update(self, shipment: Shipment) -> Shipment:
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)
        return shipment

    async def delete(self, shipment: Shipment) -> None:
        await self.session.delete(shipment)
        await self.session.commit()
