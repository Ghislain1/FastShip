# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from ..models.shipment import ShipmentBase
from uuid import UUID


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentPublic(ShipmentBase):
    id: UUID



