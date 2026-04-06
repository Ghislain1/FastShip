# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from ..models.seller import SellerBase
from uuid import UUID


class SellerCreate(SellerBase):
    password: str


class SellerPublic(SellerBase):
    id: UUID | None = None


class SellerUpdate(SellerBase):
    id: UUID | None = None
