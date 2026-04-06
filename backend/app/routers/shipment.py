from typing import Annotated

from fastapi import APIRouter, Query

from ..core.dependencies import ShipmentServiceDep
from ..schemas.shipment import ShipmentPublic


router = APIRouter(prefix="/shipment", tags=["Shipment"])


@router.get("/", response_model=list[ShipmentPublic])
async def read_all_shipments(
    shipment_service: ShipmentServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    shipments = await shipment_service.load_shipments(offset, limit)

    return shipments
