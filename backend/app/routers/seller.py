from typing import Annotated

from fastapi import APIRouter, Query

from app.core.dependencies import SellerServiceDep
from app.schemas.seller import SellerPublic

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/", response_model=list[SellerPublic])
async def read_all_seller(
    seller_service: SellerServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[SellerPublic]:
    await seller_service.all(offset, limit)
