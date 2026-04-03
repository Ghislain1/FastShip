from typing import AsyncGenerator

from passlib.context import CryptContext
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from backend.models.customer import Customer
from backend.models.order import Order, OrderStatus, PizzaSize


# POSTGRES_URL = "postgresql://postgres:namej345@localhost/pizza_deliver_db"
DATABASE_URL = "sqlite+aiosqlite:///./pizza_deliver.db"  # U must install aiosqlite


# 1. ---------------------------------------------------------- Classes --------------------------------------
class Base(SQLModel):
    pass


# 2. -------------------------------------------------------- Engine and Session  ------------------------------------
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# 3. ------------------------------ Methods ------------------------------------------
async def create_db_and_tables():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def clear_database():
    """Clear all data from database"""
    async with async_session_maker() as session:
        # Delete orders first (due to foreign key constraint)
        await session.execute("DELETE FROM order")
        # Then delete customers
        await session.execute("DELETE FROM customer")
        await session.commit()


async def generate_dummy_data():

    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    dummy_customers: list[dict[str, str]] = [
        {
            "username": "john_doe",
            "email": "john.doe@example.com",
            "password": "password123",
        },
        {
            "username": "jane_smith",
            "email": "jane.smith@example.com",
            "password": "password123",
        },
        {
            "username": "mike_johnson",
            "email": "mike.johnson@example.com",
            "password": "password123",
        },
        {
            "username": "sarah_wilson",
            "email": "sarah.wilson@example.com",
            "password": "password123",
        },
        {
            "username": "david_brown",
            "email": "david.brown@example.com",
            "password": "password123",
        },
        {
            "username": "lisa_davis",
            "email": "lisa.davis@example.com",
            "password": "password123",
        },
        {
            "username": "chris_miller",
            "email": "chris.miller@example.com",
            "password": "password123",
        },
        {
            "username": "amy_taylor",
            "email": "amy.taylor@example.com",
            "password": "password123",
        },
    ]

    async with async_session_maker() as session:
        # Create customers first
        customers = []
        for customer_data in dummy_customers:
            hashed_password = pwd_context.hash(customer_data["password"])
            customer = Customer(
                username=customer_data["username"],
                email=customer_data["email"],
                hashed_password=hashed_password,
                is_active=True,
            )
            session.add(customer)
            customers.append(customer)

        # Flush to get customer IDs
        await session.flush()

        # Create orders for each customer
        order_data = [
            # Orders for john_doe (customer_id will be set after flush)
            {
                "quantity": 2,
                "pizza_size": PizzaSize.LARGE,
                "order_status": OrderStatus.PENDING,
            },
            {
                "quantity": 1,
                "pizza_size": PizzaSize.MEDIUM,
                "order_status": OrderStatus.IN_TRANSIT,
            },
            # Orders for jane_smith
            {
                "quantity": 3,
                "pizza_size": PizzaSize.SMALL,
                "order_status": OrderStatus.DELIVERED,
            },
            # Orders for mike_johnson
            {
                "quantity": 1,
                "pizza_size": PizzaSize.EXTRA_LARGE,
                "order_status": OrderStatus.PENDING,
            },
            {
                "quantity": 2,
                "pizza_size": PizzaSize.LARGE,
                "order_status": OrderStatus.PENDING,
            },
            # Orders for sarah_wilson
            {
                "quantity": 4,
                "pizza_size": PizzaSize.MEDIUM,
                "order_status": OrderStatus.IN_TRANSIT,
            },
            # Orders for david_brown
            {
                "quantity": 1,
                "pizza_size": PizzaSize.SMALL,
                "order_status": OrderStatus.DELIVERED,
            },
            # Orders for lisa_davis
            {
                "quantity": 2,
                "pizza_size": PizzaSize.LARGE,
                "order_status": OrderStatus.PENDING,
            },
            {
                "quantity": 1,
                "pizza_size": PizzaSize.EXTRA_LARGE,
                "order_status": OrderStatus.IN_TRANSIT,
            },
            # Orders for chris_miller
            {
                "quantity": 3,
                "pizza_size": PizzaSize.MEDIUM,
                "order_status": OrderStatus.DELIVERED,
            },
            # Orders for amy_taylor
            {
                "quantity": 1,
                "pizza_size": PizzaSize.SMALL,
                "order_status": OrderStatus.PENDING,
            },
        ]

        # Assign orders to customers (distribute them)
        order_index = 0
        for i, customer in enumerate(customers):
            # Give different numbers of orders to different customers
            num_orders = [2, 1, 2, 1, 1, 2, 1, 1][i]  # john_doe:2, jane_smith:1, etc.

            for _ in range(num_orders):
                if order_index < len(order_data):
                    order_info = order_data[order_index]
                    order = Order(
                        quantity=order_info["quantity"],
                        pizza_size=order_info["pizza_size"],
                        order_status=order_info["order_status"],
                        customer_id=customer.id,
                    )
                    session.add(order)
                    order_index += 1

        await session.commit()


async def is_table_empty() -> bool:
    """Is database Empty or Not ?"""

    async with async_session_maker() as session:
        statement = select(Customer)
        response = await session.execute(statement)
        return len(response.scalars().all()) == 0
