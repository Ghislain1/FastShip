from enum import Enum as PyEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.models.order import Order  # adjust import path


class ShipmentStatus(str, PyEnum):
    """Shipment lifecycle, per Dev.md."""

    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETURNED = "returned"


class ShipmentBase(SQLModel):
    """Can be used in schema domain"""

    status: ShipmentStatus = ShipmentStatus.PENDING
    weight: float = Field(gt=0)
    destination: str = Field(min_length=1, max_length=255)
    tracking_number: str = Field(index=True, min_length=1, max_length=64)


class Shipment(ShipmentBase, table=True):
    """Represent table model  for Shipment Shipment-> Order, (1:N)"""

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    orders: list["Order"] | None = Relationship(back_populates="shipment")
