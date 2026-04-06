from uuid import UUID
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from backend.models.order import Order  # adjust import path


class ShipmentBase(SQLModel):
    """Can be used in schema domain"""

    status: str  # TODO@Ghislain1 To be improve ShipmentEvent
    weight: float
    destination: str
    tracking_number: str = Field(index=True)


class Shipment(ShipmentBase, table=True):
    """Represent table model  for Shipment Shipment-> Order, (1:N)"""

    id: UUID = Field(primary_key=True)

    orders: list["Order"] = Relationship(
        back_populates="shipment",
    )
