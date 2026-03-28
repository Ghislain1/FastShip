from sqlmodel import Relationship

from .customer import Customer
from .order import Order


# Magic: Define relationships AFTER both classes exist
Customer.orders = Relationship(back_populates="customer")
Order.customer = Relationship(back_populates="orders")

# Make Pylance happy - re-export types
__all__ = ["Customer", "Order"]
