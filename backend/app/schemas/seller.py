# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from sqlmodel import Field, SQLModel

from ..models.seller import SellerBase
from uuid import UUID


class SellerCreate(SellerBase):
    password: str = Field(min_length=4, max_length=255)


class SellerPublic(SellerBase):
    id: UUID | None = None


class SellerUpdate(SellerBase):
    id: UUID | None = None


class SellersPublic(SQLModel):
    data: list[SellerPublic]
    count: int
