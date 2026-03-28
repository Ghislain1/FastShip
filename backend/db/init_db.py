from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.db.database import (
    get_async_session,
    create_db_and_tables,
    async_session_maker,
)
from backend.models.user import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


async def seed_db_if_empty():
    # 1. Create tables ( safe if they already exist)
    await create_db_and_tables()

    # 2. Open session manually (NOT Depends)
    async with async_session_maker() as session:
        result = await session.execute(select(User).limit(1))
        user_exists = result.scalar_one_or_none()

    if user_exists:
        return  # DB got data

    # Seed  initial data
    admin = User(
        email="ghis@hallo.fr", username="POKEMON", password="admin1", is_active=True
    )
    user = User(
        email="Gem122ail@hotmail.fr",
        password="hashed_password",
        username="GHISLAIN",
    )
    users = [admin, user]
    for item in users:
        session.add(item)

    await session.commit()
