from typing import AsyncGenerator


from sqlmodel import SQLModel

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


# POSTGRES_URL = "postgresql://postgres:namej345@localhost/pizza_deliver_db"
DATABASE_URL = "sqlite+aiosqlite:///./fastshipApp.db"  # U must install aiosqlite


# 1. ---------------------------------------------------------- Classes --------------------------------------
class Base(SQLModel):
    pass


# 2. -------------------------------------------------------- Engine and Session  ------------------------------------
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# 3. ------------------------------ Methods ------------------------------------------
async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
