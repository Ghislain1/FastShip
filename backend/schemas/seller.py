# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from backend.models.seller import SellerBase
from uuid import UUID


class SellerCreate(SellerBase):
    pass


class SellerPublic(SellerBase):
    id: int


class ShipmentUpdate(SellerBase):
    id: UUID | None = None
