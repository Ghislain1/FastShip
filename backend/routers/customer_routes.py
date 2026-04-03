# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-hero
# - table model vs. data model
# table true :D

# - Create a Customer


from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from backend.core.utils import decode_access_token
from backend.schemas.customer_schema import CustomerRead
from backend.core.dependencies import CustomerServiceDep, PrinterDep
from backend.core.security import oauth2_scheme

router = APIRouter(prefix="/customers", tags=["Customers"])


# ---------------------------------------------- End points --------------------------------------------


# https://fastapi.tiangolo.com/tutorial/sql-databases/#read-heroes-with-heropublic
@router.get("/", response_model=list[CustomerRead])
async def read_all_customers(
    customer_service: CustomerServiceDep,
    printer: PrinterDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    customers = await customer_service.load_customers(offset, limit)
    printer.print_debug("=========================== read_customers ===============")
    return customers


@router.get("protect-demo")
async def get_demo_protect(
    token: Annotated[str, Depends(oauth2_scheme)],
    customer_service: CustomerServiceDep,
    printer: PrinterDep,
):
    #  by testing in Headers  add Authorization:  Bearer jjGHJSahdjklaHSDasd
    data = decode_access_token(token)

    printer.print_info("CUSTOM ROUTER", data["exp"])
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    customer_id = data["user"]["id"]

    customer = await customer_service.get_customer_by_id(customer_id)
    return customer
