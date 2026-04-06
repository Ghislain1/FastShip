# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from sqlmodel import Field

from ..models.seller import SellerBase
from uuid import UUID


class SellerCreate(SellerBase):
    password: str = Field(min_length=4, max_length=255)


class SellerPublic(SellerBase):
    id: UUID | None = None


class SellerUpdate(SellerBase):
    id: UUID | None = None
