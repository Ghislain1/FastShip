from typing import TYPE_CHECKING
from uuid import uuid4


if TYPE_CHECKING:
    from .order import Order  # adjust import path
    from .seller import Seller

from sqlmodel import UUID, Field, Relationship, SQLModel


class Product(SQLModel, table=True):
    __tablename__ = "Product"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str
    price: float
    weight: float

    orders: list["Order"] = Relationship(
        back_populates="products",
    )

    # Seller is a owner of product
    owner_id: UUID = Field(foreign_key="seller.id", nullable=False, ondelete="CASCADE")
    owner: Seller | None = Relationship(back_populates="products")
