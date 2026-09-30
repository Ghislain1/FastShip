from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Externe Libs
from prometheus_fastapi_instrumentator import Instrumentator
from scalar_fastapi import get_scalar_api_reference


from .routers.auth_routes import router as auth_router
from .routers.order_routes import router as order_router
from .routers.seller_router import router as seller_router
from .routers.shipment import router as shipment_router
from .core.config import settings
from .core.db import (
    async_session_maker,
    create_db_and_tables,
    seed_db_if_empty,
)
from .core.seed_data import seed_mock_shipments

from .core.middlewares import CustomMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # PrinterDep().print_info("MAIN", "################ Create DB AND TABLES")
    await create_db_and_tables()
    await seed_db_if_empty()

    if settings.MOCK_SEED:
        async with async_session_maker() as session:
            seeded = await seed_mock_shipments(session)
        if seeded:
            print(f"[seed] inserted {seeded} mock shipments")

    yield


app = FastAPI(lifespan=lifespan, title="FastShip")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],  # Frontend Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
