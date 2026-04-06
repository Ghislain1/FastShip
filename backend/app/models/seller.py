from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4


class SellerBase(SQLModel):
    name: str
    email: EmailStr


class Seller(SellerBase, table=True):
    """Relatiobnship One to Many with Product"""

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    rating: int | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class SellerCreate(SellerBase):
    password: str
