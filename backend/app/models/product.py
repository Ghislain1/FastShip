from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .order import Order  # adjust import path

from sqlmodel import UUID, Relationship, SQLModel


class Product(SQLModel, table=True):
    id: UUID
    title: str
    description: str
    price: float
    weight: float

    orders: list["Order"] = Relationship(
        back_populates="products",
    )
