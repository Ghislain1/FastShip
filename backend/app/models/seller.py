from typing import TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import DateTime, Relationship, SQLModel, Field
from datetime import datetime, timezone
from uuid import UUID, uuid4


if TYPE_CHECKING:
    from app.models.product import Product  # adjust import path


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class SellerBase(SQLModel):
    """Shared Properties for Seller"""

    name: str
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False


class Seller(SellerBase, table=True):
    """Relatiobnship One to Many with Product"""

    __tablename__ = "seller"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    rating: int | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),
        nullable=False,
    )
    products: list["Product"] = Relationship(back_populates="owner")
