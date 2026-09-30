# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from uuid import UUID

from sqlmodel import Field, SQLModel

from ..models.shipment import ShipmentBase, ShipmentStatus


class ShipmentCreate(ShipmentBase):
    """Create payload. All fields come from ShipmentBase."""


class ShipmentUpdate(SQLModel):
    """Partial update payload. Only the fields that are set will change."""

    status: ShipmentStatus | None = None
    weight: float | None = Field(default=None, gt=0)
    destination: str | None = Field(default=None, min_length=1, max_length=255)
    tracking_number: str | None = Field(default=None, min_length=1, max_length=64)


class ShipmentPublic(ShipmentBase):
    id: UUID


class ShipmentsPublic(SQLModel):
    data: list[ShipmentPublic]
    count: int
