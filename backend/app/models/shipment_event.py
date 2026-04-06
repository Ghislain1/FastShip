from __future__ import annotations
from uuid import uuid4, UUID
from sqlmodel import Field
from sqlmodel import SQLModel


class ShipmentEvent(SQLModel, table=True):
    """Shipment event Table"""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    location: int
    status: str
    decription: str
