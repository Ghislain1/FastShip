from typing import AsyncGenerator


from sqlmodel import SQLModel, select

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from backend.app.models.seller import Seller
from backend.app.schemas.seller import SellerCreate
from backend.app.services.seller_service import SellerService

from ..core.config import settings


# 1. ---------------------------------------------------------- Classes --------------------------------------
class Base(SQLModel):
    pass


# 2. -------------------------------------------------------- Engine and Session  ------------------------------------
engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# 3. ------------------------------ Methods ------------------------------------------
async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def seed_db_if_empty() -> None:
    """TODO: To be move on top due to service"""
    async with async_session_maker() as session:
        statement_seller = select(Seller).where(
            Seller.email == settings.FIRST_SUPERUSER
        )
        super_user = await session.execute(statement_seller)
        if super_user is not None:
            return
        user_service = SellerService(session)
        await user_service.add_seller(
            SellerCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
        )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
