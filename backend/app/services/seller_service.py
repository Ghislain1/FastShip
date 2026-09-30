#  passlib[bcrypt] must be installed
from passlib.context import CryptContext
from fastapi.exceptions import HTTPException
from starlette import status

from ..core.utils import generate_access_token

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.seller import Seller

from ..repositories.seller_repository import SellerRepository

from ..schemas.seller import SellerCreate


class SellerService:
    """Use AsyncSession to Manage DB"""

    def __init__(self, session: AsyncSession):
        # Argon2 (no length limit, more modern)
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.session = session
        self.repository = SellerRepository(session)

    async def add_seller(self, seller_create: SellerCreate) -> Seller:
        """Create a new seller with hashed password"""

        # Check for duplicate email
        existing = await self.repository.get_by_email(seller_create.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A seller with this email already exists",
            )

        # Hash the plain password
        hashed_password = self.pwd_context.hash(seller_create.password)

        # Create DB model
        seller_data = seller_create.model_dump()
        seller_data.pop("password", None)
        db_seller = Seller(**seller_data, hashed_password=hashed_password)
        return await self.repository.add(db_seller)

    async def all(self, offset: int, limit: int) -> list[Seller]:
        """Load all sellers from database"""

        return await self.repository.list(offset, limit)

    async def get_sellers_count(self) -> int:
        """Provide the  total number of sellers"""

        return await self.repository.count()

    # @TODO
    async def get_seller_by_email(self, email: str):
        """Get seller  from database"""
        db_seller = await self.repository.get_by_email(email)

        if db_seller is not None:
            return HTTPException(402, detail="email is already used!..")

        #  Check name

        return db_seller

    async def token(self, email, password) -> str:
        """Valide the credentials"""

        seller = await self.repository.get_by_email(email)

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
                "name": seller.name,
                "email": seller.email,
                "id": str(seller.id),  # because UUID is not serializable
            }
        }

        tk = generate_access_token(data)

        return {"access_token": tk, "type": "jwt"}

    async def get_seller_by_id(self, id):
        db_seller = await self.repository.get_by_id(id)
        if db_seller is None:
            raise HTTPException(402, detail="email is already used!..")
        return db_seller
