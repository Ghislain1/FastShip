# #https://github.com/fastapi/full-stack-fastapi-template/blob/master/backend/app/api/routes/users.py

from typing import Annotated
from fastapi import APIRouter, Query
from ..core.dependencies import SellerServiceDep
from ..schemas.seller import SellerPublic, SellersPublic

router = APIRouter(prefix="/sellers", tags=["Sellers[Users]"])


@router.get("/", response_model=SellersPublic)
async def read_sellers(
    seller_service: SellerServiceDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> any:

    count = await seller_service.get_sellers_count()
    sellers = await seller_service.all(offset, limit)
    sellers_public = [SellerPublic.model_validate(seller) for seller in sellers]
    return SellersPublic(data=sellers_public, count=count)
