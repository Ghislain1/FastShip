import os
import sys
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.core.db import get_async_session
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(autouse=True)
def fast_password_hashing(monkeypatch):
    """Keep argon2 in the tests, but at negligible cost.

    Production hashing parameters are deliberately expensive. Most API tests
    only need *a* hash to verify against, and paying real argon2 cost once per
    test dominated the suite runtime.
    """
    from app.services import seller_service

    def cheap_context(*args, **kwargs):
        kwargs.setdefault("schemes", ["argon2"])
        kwargs.setdefault("argon2__time_cost", 1)
        kwargs.setdefault("argon2__memory_cost", 8)
        kwargs.setdefault("argon2__parallelism", 1)
        return CryptContext(*args, **kwargs)

    monkeypatch.setattr(seller_service, "CryptContext", cheap_context)


@pytest_asyncio.fixture(scope="function")
async def db():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
def client():
    return TestClient(app)


@pytest_asyncio.fixture
async def test_client(db: AsyncSession):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_async_session] = override_get_db
    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.clear()
