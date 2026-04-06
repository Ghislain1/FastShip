from contextlib import asynccontextmanager

from fastapi import FastAPI

# Externe Libs
from prometheus_fastapi_instrumentator import Instrumentator
from scalar_fastapi import get_scalar_api_reference


from app.routers.auth_routes import router as auth_router
from app.routers.order_routes import router as order_router
from app.routers.seller import router as seller_router
from app.routers.shipment import router as shipment_router
from app.core.db import create_db_and_tables, seed_db_if_empty

from app.core.middlewares import CustomMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # PrinterDep().print_info("MAIN", "################ Create DB AND TABLES")
    await create_db_and_tables()
    await seed_db_if_empty()

    yield


app = FastAPI(lifespan=lifespan, title="FastShip")

# Create behing the scene endpoint /metrics
Instrumentator().instrument(app=app).expose(app=app)

# Add Middlewares
app.add_middleware(CustomMiddleware)

# Include router from different API
app.include_router(auth_router)
app.include_router(shipment_router)
app.include_router(order_router)
app.include_router(seller_router)


@app.get("/")
def root():
    return {"Hello welcome to my first FastAPI real world Project called Delivery API"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url)
