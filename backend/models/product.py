from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from backend.models.order import Order  # adjust import path

from sqlmodel import UUID, Column, Field, Relationship, SQLModel, String


class Product(SQLModel, table=True):
    id: UUID
    title: str
    description: str
    price: float
    weight: float

    orders: list["Order"] = Relationship(
        back_populates="products",
    )
