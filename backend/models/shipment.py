from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from backend.models.order import Order


class ShipmentBase(SQLModel):
    """Can be used in schema domain"""

    status: str  # TODO@Ghislain1 To be improve ShipmentEvent
    weight: float
    destination: str
    tracking_number: str = Field(index=True)


class Shipment(ShipmentBase, table=True):
    """Represent table model  for Shipment"""

    id: UUID = Field(primary_key=True)

    orders: list[Order] = Relationship(
        back_populates="shipments",
    )
