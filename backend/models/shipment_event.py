from datetime import datetime
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from backend.models.order import Order


class ShipmentEvent(SQLModel, table=True):
    """Shipment event Table"""

    id: UUID
    location: int
    status: str
    decription: str
