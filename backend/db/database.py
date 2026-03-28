from typing import AsyncGenerator


from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


POSTGRES_URL = "postgresql://postgres:namej345@localhost/pizza_deliver_db"
DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # U must install aiosqlite
SQLITE_URL = "sqlite:///./pizza_deliver.db"

# engine = create_engine(SQLITE_URL, echo=True, connect_args={"check_same_thread": False})


# ---------------------------------------------------------- Classes --------------------------------------
class Base(DeclarativeBase):
    pass


# -------------------------------------------------------- Engine and Session  ------------------------------------
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# ------------------------------ Methods ------------------------------------------
async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
