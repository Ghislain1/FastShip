# https://fastapi.tiangolo.com/tutorial/sql-databases/#create-an-engine


from sqlmodel import Session, create_engine, SQLModel, select

from backend.models.customer import Customer
from backend.models.order import Order
from backend.models.order_status import OrderStatus

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}


engine = create_engine(sqlite_url, connect_args=connect_args)


# ------------------------------------- Function ------------------------
async def create_db_and_tables():
    """Create the tables for all table models ( Customer table, Order Table)"""
    SQLModel.metadata.create_all(engine)


# Unit of work pattern
def get_session():
    with Session(engine) as session:
        yield session  # to learn  yield in paython again


async def seed_db_if_empty() -> None:
    with Session(engine) as session:
        # check if there are any customers already
        customers_count = session.exec(select(Customer)).first()
        if customers_count:
            return  # DB has data, do nothing

        # create 5 customers
        customers = [
            Customer(
                username="Alice",
                email="alice@example.com",
                hashed_password="$2b$12$Kix...!@@@@@5",
            ),
            Customer(
                username="Bob",
                email="bob@example.com",
                hashed_password="$2b$12$Kix...!@@@@@4",
            ),
            Customer(
                username="Carol",
                email="carol@example.com",
                hashed_password="$2b$12$Kix...!@@@@@3",
            ),
            Customer(
                username="Dave",
                email="dave@example.com",
                hashed_password="$2b$12$Kix...!@@@@@2",
            ),
            Customer(
                username="Eve",
                email="eve@example.com",
                hashed_password="$2b$12$Kix...!@@@@@1",
            ),
        ]
        session.add_all(customers)
        session.commit()
        # refresh to get IDs
        for c in customers:
            session.refresh(c)

        # create 3 orders for the first 3 customers
        orders = [
            Order(order_status=OrderStatus.PENDING, customer_id=customers[0].id),
            Order(order_status=OrderStatus.IN_TRANSIT, customer_id=customers[1].id),
            Order(order_status=OrderStatus.DELIVERED, customer_id=customers[2].id),
        ]
        session.add_all(orders)
        session.commit()
