# from typing import Optional
from enum import Enum as PyEnum
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from backend.app.models.shipment import Shipment


# Enum for order status
class OrderStatus(str, PyEnum):
    PENDING = "pending"
    IN_TRANSIT = "in-transit"
    DELIVERED = "delivered"


class OrderBase(SQLModel):
    created_at: datetime
    updated_at: datetime
    quantity: int = Field(default=1)


class Order(OrderBase, table=True):
    """Relationship (1 : N)"""

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # product_id: UUID = Field(foreign_key="product.id", primary_key=True)

    shipment: "Shipment" = Relationship(back_populates="orders")
    shipment_id: UUID = Field(
        foreign_key="shipment.id", nullable=False, ondelete="CASCADE"
    )
