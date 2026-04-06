# Singleton using @lru_cache
from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from .db import get_async_session
from ..services.seller_service import SellerService
from ..services.shipment_service import ShipmentService
from ..services.order_service import OrderService
from ..services.printer_service import PrinterService
from sqlalchemy.ext.asyncio import AsyncSession


@lru_cache
def get_seller_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return SellerService(session=session)


@lru_cache
def get_order_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return OrderService(session=session)


@lru_cache
def get_printer_service():
    return PrinterService()


@lru_cache
def get_shipment_service(session: Annotated[AsyncSession, Depends(get_async_session)]):
    return ShipmentService(session)


# AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]
