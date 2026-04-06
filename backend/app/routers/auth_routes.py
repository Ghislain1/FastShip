from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

# Own import
from ..core.dependencies import SellerServiceDep
from ..schemas.seller import SellerCreate, SellerPublic

# Router definition for Authentication
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
async def login_seller(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    seller_service: SellerServiceDep,
):
    username = form_data.username
    password = form_data.password

    return await seller_service.token(username, password=password)


# To Register a seller
@router.post("/signup", response_model=SellerPublic)
async def register_seller(
    seller_create: SellerCreate, seller_service: SellerServiceDep
):

    return await seller_service.add_seller(seller_create)
