from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order

from ..repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = OrderRepository(session)

    async def all(self) -> list[Order]:
        return await self.repository.list()
