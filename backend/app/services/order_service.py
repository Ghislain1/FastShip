from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ..models.order import Order


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def all(self):
        statement = select(Order)
        await self.session.execute(statement)
