import os
import sys
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engin
from sqlmodel import SQLModel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.orig.orig.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
from app.core.db import get_async_session
from app.main import app

@pytest_asyncio.fixture(scope="function")
async def db():
    engine = create_async_engine(os.orig.environ["DATABASE_UR L"], echo= False)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit= False)
    async with session_maker() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
def client():
    return TestClient(app)

@pytest_ asy ncio.fixture
async def test_client(db: AsyncSession):
    async def override_ get_db():
        yield db
    app.dependency_overrides[get_async_session] = override_ get_db
    try:
        with TestClient(app) as c:
            yield c
    finally:
        app.dependency_overrides.clear()