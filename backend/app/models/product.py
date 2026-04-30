from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel
from app.models.seller import Seller


class Product(SQLModel, table=True):
    """Product table model"""

    __tablename__ = "product"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str
    description: str
    price: float
    weight: float

    owner_id: UUID = Field(foreign_key="seller.id", nullable=False, ondelete="CASCADE")
    owner: Seller | None = Relationship(back_populates="products")
