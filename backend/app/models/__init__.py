# from sqlmodel import Relationship

# from .customer import Customer
# from .order import Order


# Magic: Define relationships AFTER both classes exist
# Customer.orders = Relationship(back_populates="customer")
# Order.customer = Relationship(back_populates="orders")

# Make Pylance happy - re-export types
# __all__ = ["Customer", "Order"]

from backend.app.models.seller import Seller
from backend.app.models.product import Product
from backend.app.models.order import Order
from backend.app.models.shipment import Shipment
from backend.app.models.shipment_event import ShipmentEvent

# TODO@Ghis why do you do that?
# __all__ = [Seller, Product, Order, Shipment, ShipmentEvent]
