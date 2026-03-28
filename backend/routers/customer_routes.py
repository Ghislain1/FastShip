# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-hero
# - table model vs. data model
# table true :D

# - Create a Customer


from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from backend.db import get_session
from backend.schemas.custom_schema import CustomerCreate, CustomerPublic
from backend.services.customer_service import CustomerService
from backend.core.dependencies import PrinterDep


router = APIRouter(prefix="/customers", tags=["Customers"])

# Main Goal to convert table model to data model
customer_service = CustomerService()


# ---------------------------------------------- End points --------------------------------------------
@router.post("/", response_model=CustomerPublic)
def create_customer(
    customer: CustomerCreate, session: Annotated[Session, Depends(get_session)]
):
    db_custom = customer_service.create_customer(
        customer_create=customer, session=session
    )

    return db_custom


# https://fastapi.tiangolo.com/tutorial/sql-databases/#read-heroes-with-heropublic
@router.get("/", response_model=list[CustomerPublic])
def read_customers(
    session: Annotated[Session, Depends(get_session)],
    printer: PrinterDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    customers = customer_service.load_customers(session, offset, limit)
    printer.print_debug(
        "================================================= read_customers ==============="
    )
    return customers
