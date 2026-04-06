#  passlib[bcrypt] must be installed
from passlib.context import CryptContext
from sqlmodel import select
from fastapi.exceptions import HTTPException
from starlette import status

from app.core.utils import generate_access_token

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.shipment import Shipment
from app.schemas.shipment import ShipmentCreate


class ShipmentService:
    def __init__(self, session: AsyncSession):
        # Argon2 (no length limit, more modern)
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.session = session

    async def create_shipment(self, customer_create: ShipmentCreate) -> Shipment:
        """Create a new customer with hashed password"""
        # Hash the plain password
        hashed_password = self.pwd_context.hash(customer_create.password)

        # Create DB model
        # Magic: model_validate copies fields + adds hashed_password
        db_customer = Shipment.model_validate(
            customer_create, update={"hashed_password": hashed_password}
        )
        self.session.add(db_customer)
        await self.session.commit()
        await self.session.refresh(db_customer)
        return db_customer

    async def load_shipments(self, offset: int, limit: int) -> list[Shipment]:
        """Load all customers from database"""

        statement = select(Shipment).offset(offset).limit(limit)
        results = await self.session.execute(statement=statement)
        customers = results.scalars().all()
        return customers

    # @TODO
    def get_customer_by_email(self, email: str):
        """Get Customer  from database"""
        statement = select(Shipment)
        db_customer = self.session.exec(
            statement.filter(Shipment.email == email).first()
        )

        if db_customer is not None:
            return HTTPException(402, detail="email is already used!..")

        #  Check name

        return db_customer

    async def token(self, email, password) -> str:
        """Valide the credentials"""

        condition_on_email = Shipment.email == email
        # Select the table like the name of method @TODO Ghis select from sqlmodel
        statement = select(Shipment).where(condition_on_email)

        result = await self.session.execute(statement=statement)

        customer = result.scalar()

        if customer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[Ghis]> The Customer with that email is not found!!",
            )

        # Check Password
        is_ok = self.pwd_context.verify(password, customer.hashed_password)
        if not is_ok:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[Ghis]> The Customer with that Password is incorrect!",
            )

        # Data
        data = {
            "user": {
                "name": customer.username,
                "email": customer.email,
                "id": customer.id,
            }
        }

        tk = generate_access_token(data)

        return {"access_token": tk, "type": "jwt"}

    async def get_customer_by_id(self, id: int):
        db_customer = await self.session.get(Shipment, id)
        if db_customer is None:
            raise HTTPException(402, detail="email is already used!..")
        return db_customer
