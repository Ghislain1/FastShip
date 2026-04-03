from fastapi import APIRouter, Depends

from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

# Own import
from backend.core.dependencies import SellerServiceDep

from backend.schemas.customer_schema import CustomerRead
from backend.schemas.seller import SellerCreate

# Router definition for Authentication
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
async def login_customer(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    seller_service: SellerServiceDep,
):
    username = form_data.username
    password = form_data.password

    return await seller_service.token(username, password=password)


# To Register a customer
@router.post("/signup", response_model=CustomerRead)
async def register_customer(
    customer_create: SellerCreate, customer_service: SellerServiceDep
):

    return await customer_service.create_customer(customer_create)
