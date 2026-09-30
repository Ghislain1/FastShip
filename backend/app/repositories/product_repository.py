from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.product import Product


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> list[Product]:
        result = await self.session.execute(select(Product))
        return list(result.scalars().all())

    async def add(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product
