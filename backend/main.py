from contextlib import asynccontextmanager

from fastapi import FastAPI

# Externe Libs
from prometheus_fastapi_instrumentator import Instrumentator

# Pizza
from backend.db import create_db_and_tables, seed_db_if_empty
from backend.routers.auth_routes import router as auth_router
from backend.routers.order_routes import router as order_router
from backend.routers.customer_routes import router as customer_router
from backend.core.middlewares import CustomMiddleware

from backend.core.dependencies import get_printer_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    get_printer_service().print_debug("Create DB AND TABLES")
    await seed_db_if_empty()

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
