from fastapi import APIRouter, Depends

from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from ..core.dependencies import OrderServiceDep
from ..core.security import oauth2_scheme
from ..schemas.order_schema import OrderPublic


# fastapi_jwt_auth must be installed

# tags ist for documentation title
router = APIRouter(prefix="/order", tags=["Orders"])


@router.get("/user/order/{id}/")
async def get_specific_order(
    id: int, authorize: Annotated[OAuth2PasswordBearer, Depends(oauth2_scheme)]
):
    return {"id": id, "authorize": authorize}


@router.get("/", response_model=list[OrderPublic])
async def get_all_orders(order_service: OrderServiceDep):
    await order_service.all()
