# https://sqlmodel.tiangolo.com/tutorial/fastapi/relationships/#models-with-relationships

from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class SellerCreate(SQLModel):
    """Public signup payload.

    Deliberately does NOT inherit SellerBase: inheriting it would expose
    `is_superuser` and `is_active` as client-settable fields.
    """

    name: str
    email: EmailStr
    password: str = Field(min_length=4, max_length=255)


class SellerPublic(SQLModel):
    """Public seller representation.

    `is_superuser` is intentionally not exposed.
    """

    id: UUID | None = None
    name: str
    email: EmailStr
    is_active: bool


class SellersPublic(SQLModel):
    data: list[SellerPublic]
    count: int
