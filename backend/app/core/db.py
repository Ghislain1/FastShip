from typing import AsyncGenerator


from sqlmodel import SQLModel, select

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.models.seller import Seller
from app.schemas.seller import SellerCreate
from app.services.seller_service import SellerService

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
    """Seed database with first superuser if it doesn't exist"""
    async with async_session_maker() as session:
        # Check if superuser already exists
        super_user = await session.scalar(
            select(Seller).where(Seller.email == settings.FIRST_SUPERUSER)
        )
        if super_user is not None:
            return

        # Create first superuser
        user_service = SellerService(session)
        await user_service.add_seller(
            SellerCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                name=settings.FIRST_SUPERUSER_NAME,
                is_superuser=True,
            )
        )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
