from typing import Annotated
from fastapi import Depends
from .db import get_async_session
from ..repositories.seller_repository import SellerRepository
from ..repositories.order_repository import OrderRepository
from ..repositories.shipment_repository import ShipmentRepository
from ..services.seller_service import SellerService
from ..services.shipment_service import ShipmentService
from ..services.order_service import OrderService
from sqlalchemy.ext.asyncio import AsyncSession


def get_seller_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> SellerRepository:
    return SellerRepository(session)


def get_order_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> OrderRepository:
    return OrderRepository(session)


def get_shipment_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ShipmentRepository:
    return ShipmentRepository(session)


def get_seller_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> SellerService:
    return SellerService(session=session)


def get_order_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> OrderService:
    return OrderService(session=session)


def get_shipment_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> ShipmentService:
    return ShipmentService(session=session)


# AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
OrderServiceDep = Annotated[OrderService, Depends(get_order_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]

SellerRepositoryDep = Annotated[SellerRepository, Depends(get_seller_repository)]
OrderRepositoryDep = Annotated[OrderRepository, Depends(get_order_repository)]
ShipmentRepositoryDep = Annotated[ShipmentRepository, Depends(get_shipment_repository)]
