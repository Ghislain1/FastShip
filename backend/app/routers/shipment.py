from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, Query, Response, status

from ..core.dependencies import ShipmentServiceDep
from ..core.security import CurrentSellerDep
from ..models.shipment import ShipmentStatus
from ..schemas.shipment import (
    ShipmentCreate,
    ShipmentPublic,
    ShipmentsPublic,
    ShipmentUpdate,
)

router = APIRouter(prefix="/shipments", tags=["Shipments"])

SortBy = Literal["tracking_number", "destination", "weight", "status"]

OrderQuery = Annotated[
    bool,
    Query(description="Sort descending when true, ascending when false"),
]


@router.get("", response_model=ShipmentsPublic, summary="List shipments")
async def list_shipments(
    shipment_service: ShipmentServiceDep,
    current_seller: CurrentSellerDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
    status_filter: Annotated[ShipmentStatus | None, Query(alias="status")] = None,
    destination: Annotated[str | None, Query(max_length=255)] = None,
    sort_by: Annotated[SortBy, Query(description="Sort field")] = "tracking_number",
    descending: OrderQuery = False,
) -> ShipmentsPublic:
    """Paginated shipments, optionally filtered and sorted.

    The filters are an allow-listed enum and a plain literal comparison, so no
    user input ever reaches the query builder as SQL.
    """
    count = await shipment_service.count_shipments(
        status_filter=status_filter, destination=destination
    )
    shipments = await shipment_service.load_shipments(
        offset,
        limit,
        status_filter=status_filter,
        destination=destination,
        sort_by=sort_by,
        descending=descending,
    )

    return ShipmentsPublic(
        data=[ShipmentPublic.model_validate(s) for s in shipments], count=count
    )


@router.post(
    "",
    response_model=ShipmentPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a shipment",
)
async def create_shipment(
    shipment_create: ShipmentCreate,
    shipment_service: ShipmentServiceDep,
    current_seller: CurrentSellerDep,
) -> ShipmentPublic:
    shipment = await shipment_service.create_shipment(shipment_create)
    return ShipmentPublic.model_validate(shipment)


@router.get(
    "/{shipment_id}",
    response_model=ShipmentPublic,
    summary="Get one shipment",
    responses={404: {"description": "Shipment not found"}},
)
async def get_shipment(
    shipment_id: UUID,
    shipment_service: ShipmentServiceDep,
    current_seller: CurrentSellerDep,
) -> ShipmentPublic:
    shipment = await shipment_service.get_shipment_by_id(shipment_id)
    return ShipmentPublic.model_validate(shipment)


@router.patch(
    "/{shipment_id}",
    response_model=ShipmentPublic,
    summary="Partially update a shipment",
    responses={404: {"description": "Shipment not found"}},
)
async def patch_shipment(
    shipment_id: UUID,
    shipment_update: ShipmentUpdate,
    shipment_service: ShipmentServiceDep,
    current_seller: CurrentSellerDep,
) -> ShipmentPublic:
    shipment = await shipment_service.update_shipment(shipment_id, shipment_update)
    return ShipmentPublic.model_validate(shipment)


@router.put(
    "/{shipment_id}",
    response_model=ShipmentPublic,
    summary="Replace a shipment",
    responses={404: {"description": "Shipment not found"}},
)
async def put_shipment(
    shipment_id: UUID,
    shipment_create: ShipmentCreate,
    shipment_service: ShipmentServiceDep,
    current_seller: CurrentSellerDep,
) -> ShipmentPublic:
    """Full replace. Fields absent from the body fall back to their defaults."""
    shipment = await shipment_service.update_shipment(
        shipment_id, ShipmentUpdate.model_validate(shipment_create.model_dump())
    )
    return ShipmentPublic.model_validate(shipment)


@router.delete(
    "/{shipment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a shipment and its orders",
    responses={
        404: {"description": "Shipment not found"},
        204: {"description": "Deleted, including any attached orders"},
    },
)
async def delete_shipment(
    shipment_id: UUID,
    shipment_service: ShipmentServiceDep,
    current_seller: CurrentSellerDep,
) -> Response:
    await shipment_service.delete_shipment(shipment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
