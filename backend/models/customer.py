from typing import Optional, List, TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from backend.models.order import Order  # adjust import path

from sqlmodel import Column, Field, Relationship, String

from backend.models.base import EntityBase


# All fields that are shared by models
class CustomBase(EntityBase):
    """Means : Pydantic can used it too, SQLAlchemy can use it too"""

    # Colunm Name in table
    username: Optional[str] = Field(default="unknow name ", unique=True, max_length=155)


# This is a table model not a data model ( see schema)
class Customer(CustomBase, table=True):
    # Column email in sqlModel with EmailStr validataion
    email: EmailStr = Field(
        sa_column=Column(
            String(255),
            unique=True,
            index=True,
            nullable=False,
        )
    )

    # Best Pratice  to store password as hashed string
    hashed_password: str = Field(unique=True, nullable=False)
    is_staff: Optional[bool] = Field(default=False)
    is_active: Optional[bool] = Field(default=False)

    # Relation :  one cutomer -->  many orders *** Pylance provides Error  due to Order why?****
    orders: List["Order"] = Relationship(back_populates="customer")

    def __repr__(self):
        return f"<User {self.username} - {self.email}"
