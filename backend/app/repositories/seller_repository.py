from uuid import UUID

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.seller import Seller


class SellerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: UUID) -> Seller | None:
        return await self.session.get(Seller, id)

    async def get_by_email(self, email: str) -> Seller | None:
        statement = select(Seller).where(Seller.email == email)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def list(self, offset: int, limit: int) -> list[Seller]:
        statement = select(Seller).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def count(self) -> int:
        statement = select(func.count()).select_from(Seller)
        return await self.session.scalar(statement)

    async def add(self, seller: Seller) -> Seller:
        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
