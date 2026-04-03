from contextlib import asynccontextmanager

from fastapi import FastAPI

# Externe Libs
from prometheus_fastapi_instrumentator import Instrumentator
from scalar_fastapi import get_scalar_api_reference

# Pizza

from backend.db.database import (
    create_db_and_tables,
    generate_dummy_data,
    is_table_empty,
)
from backend.routers.auth_routes import router as auth_router
from backend.routers.order_routes import router as order_router
from backend.routers.customer_routes import router as customer_router
from backend.core.middlewares import CustomMiddleware

from backend.core.dependencies import PrinterDep


@asynccontextmanager
async def lifespan(app: FastAPI):
    PrinterDep().print_info("MAIN", "################ Create DB AND TABLES")
    await create_db_and_tables()
    empty = await is_table_empty()
    if empty:
        await generate_dummy_data()

    yield


app = FastAPI(lifespan=lifespan, title="PizzaDeliveryApp")

# Create behing the scene endpoint /metrics
Instrumentator().instrument(app=app).expose(app=app)

# Add Middlewares
app.add_middleware(CustomMiddleware)

# Include router from different API
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(customer_router)


@app.get("/")
def root():
    return {"Hello welcome to my first FastAPI real world Project called Delivery API"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
