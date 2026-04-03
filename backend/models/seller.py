from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID


class SellerBase(SQLModel):
    name: str
    email: EmailStr
    created_at: datetime
    rating: int
    password_hashed: str


class Seller(SellerBase, table=True):
    """Relatiobnship One to Many with Product"""

    id: UUID = Field(primary_key=True)
