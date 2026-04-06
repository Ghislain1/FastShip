from uuid import UUID

from sqlmodel import SQLModel


class ShipmentEvent(SQLModel, table=True):
    """Shipment event Table"""

    id: UUID
    location: int
    status: str
    decription: str
