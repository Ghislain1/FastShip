from enum import Enum


# Enum for order status
class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_TRANSIT = "in-transit"
    DELIVERED = "delivered"
