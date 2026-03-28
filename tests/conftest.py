import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from backend.main import app
# from app.models import Customer, Order  # Import your models too

# In-memory SQLite
SQLITE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLITE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)


@pytest.fixture(scope="function", autouse=True)
def session():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session):
    def override_get_session():
        return session

    # Fix: Override your actual dependency function
    # Replace 'get_session' with your real function name from app/database.py
    if "get_session" in app.dependency_overrides:
        app.dependency_overrides["get_session"] = override_get_session
    else:
        # Common FastAPI pattern
        from backend.db import get_session as get_db_session

        app.dependency_overrides[get_db_session] = override_get_session

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
