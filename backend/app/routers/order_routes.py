from fastapi import APIRouter

from ..core.dependencies import OrderServiceDep
from ..core.security import CurrentSellerDep
from ..schemas.order_schema import OrderPublic


# tags ist for documentation title
router = APIRouter(prefix="/order", tags=["Orders"])


@router.get("/user/order/{id}/")
async def get_specific_order(id: int, current_seller: CurrentSellerDep):
    return {"id": id}


@router.get("/", response_model=list[OrderPublic])
async def get_all_orders(
    order_service: OrderServiceDep, current_seller: CurrentSellerDep
):
    # NOTE@Phase2: missing `return` -> always 500. Left as-is to keep the
    # phase boundary; fixing it needs the OrderPublic model fix too.
    await order_service.all()
