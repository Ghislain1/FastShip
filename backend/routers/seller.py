from fastapi import APIRouter

from backend.core.dependencies import SellerServiceDep
from backend.schemas.seller import SellerPublic

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.get("/", response_model=list[SellerPublic])
async def read_all_seller(seller_service: SellerServiceDep) -> list[SellerPublic]:
    await seller_service.all()
