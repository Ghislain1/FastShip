# from sqlmodel import Relationship

# from .customer import Customer
# from .order import Order


# Magic: Define relationships AFTER both classes exist
# Customer.orders = Relationship(back_populates="customer")
# Order.customer = Relationship(back_populates="orders")

# Make Pylance happy - re-export types
# __all__ = ["Customer", "Order"]

from app.models.seller import Seller
from app.models.product import Product
from app.models.order import Order
from app.models.shipment import Shipment
from app.models.shipment_event import ShipmentEvent

# TODO@Ghis why do you do that?
__all__ = [Seller, Product, Order, Shipment, ShipmentEvent]
