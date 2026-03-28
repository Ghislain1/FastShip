#  passlib[bcrypt] must be installed
from passlib.context import CryptContext
from sqlmodel import Session, select

from backend.models.customer import Customer
from backend.schemas.custom_schema import CustomerCreate


class CustomerService:
    def __init__(self):
        # Argon2 (no length limit, more modern)
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def create_customer(self, customer_create: CustomerCreate, session: Session):
        """Create a new customer with hashed password"""
        # Hash the plain password
        hashed_password = self.pwd_context.hash(customer_create.password)

        # Create DB model
        # Magic: model_validate copies fields + adds hashed_password
        db_customer = Customer.model_validate(
            customer_create, update={"hashed_password": hashed_password}
        )
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

    def load_customers(self, session: Session, offset: int, limit: int):
        """Load all customers from database"""
        statement = select(Customer)
        customers = session.exec(statement.offset(offset).limit(limit)).all()
        return customers
