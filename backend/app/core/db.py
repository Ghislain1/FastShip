from datetime import datetime
from typing import AsyncGenerator
from uuid import uuid4

from sqlmodel import SQLModel, select

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from ..core.config import settings
from ..models.order import Order
from ..models.shipment import Shipment


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
    async with async_session_maker() as session:
        existing_shipment_id = await session.scalar(select(Shipment.id).limit(1))
        if existing_shipment_id is not None:
            return

        shipments = []
        for index in range(1, 12):
            shipment_id = uuid4()
            shipment = Shipment(
                id=shipment_id,
                status="pending",
                weight=1.0 + index,
                destination=f"Address {index}",
                tracking_number=f"TRACK{index:04d}",
            )
            order = Order(
                id=uuid4(),
                shipment_id=shipment_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                quantity=1,
            )
            shipment.orders = [order]
            shipments.append(shipment)

        session.add_all(shipments)
        await session.commit()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
