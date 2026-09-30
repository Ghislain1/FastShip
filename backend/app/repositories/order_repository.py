from uuid import UUID

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Order | None:
        return await self.session.get(Order, id)

    async def list(self) -> list[Order]:
        result = await self.session.execute(select(Order))
        return list(result.scalars().all())

    async def count(self) -> int:
        statement = select(func.count()).select_from(Order)
        return await self.session.scalar(statement)

    async def add(self, order: Order) -> Order:
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order
