#  passlib[bcrypt] must be installed
from passlib.context import CryptContext
from sqlmodel import select
from fastapi.exceptions import HTTPException
from starlette import status

from backend.core.utils import generate_access_token

from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.seller import Seller

from backend.schemas.seller import SellerCreate


class SellerService:
    """Use AsyncSession to Manage DB"""

    def __init__(self, session: AsyncSession):
        # Argon2 (no length limit, more modern)
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.session = session

    async def add_seller(self, seller_create: SellerCreate) -> Seller:
        """Create a new seller with hashed password"""
        # Hash the plain password
        hashed_password = self.pwd_context.hash(seller_create.password)

        # Create DB model
        # Magic: model_validate copies fields + adds hashed_password
        db_seller = Seller.model_validate(
            seller_create, update={"hashed_password": hashed_password}
        )
        self.session.add(db_seller)
        await self.session.commit()
        await self.session.refresh(db_seller)
        return db_seller

    async def all(self, offset: int, limit: int) -> list[Seller]:
        """Load all sellers from database"""

        statement = select(Seller).offset(offset).limit(limit)
        results = await self.session.execute(statement=statement)
        sellers = results.scalars().all()
        return sellers

    # @TODO
    def get_seller_by_email(self, email: str):
        """Get seller  from database"""
        statement = select(Seller)
        db_seller = self.session.exec(statement.filter(Seller.email == email).first())

        if db_seller is not None:
            return HTTPException(402, detail="email is already used!..")

        #  Check name

        return db_seller

    async def token(self, email, password) -> str:
        """Valide the credentials"""

        condition_on_email = Seller.email == email
        # Select the table like the name of method @TODO Ghis select from sqlmodel
        statement = select(Seller).where(condition_on_email)

        result = await self.session.execute(statement=statement)

        seller = result.scalar()

        if seller is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[Ghis]> The seller with that email is not found!!",
            )

        # Check Password
        is_ok = self.pwd_context.verify(password, seller.hashed_password)
        if not is_ok:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="[Ghis]> The seller with that Password is incorrect!",
            )

        # Data
        data = {
            "user": {
                "name": seller.username,
                "email": seller.email,
                "id": seller.id,
            }
        }

        tk = generate_access_token(data)

        return {"access_token": tk, "type": "jwt"}

    async def get_seller_by_id(self, id: int):
        db_seller = await self.session.get(Seller, id)
        if db_seller is None:
            raise HTTPException(402, detail="email is already used!..")
        return db_seller
