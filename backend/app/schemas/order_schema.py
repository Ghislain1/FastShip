from typing import Optional


from app.models.order import OrderBase, OrderStatus


class OrderPublic(OrderBase):
    """Order response model"""

    quantity: int
    order_status: OrderStatus
    customer_id: Optional[int] = None
