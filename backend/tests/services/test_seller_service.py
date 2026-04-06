import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.schemas.seller import SellerCreate
from backend.app.services.seller_service import SellerService
from backend.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_seller(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    username = random_lower_string()
    seller_in = SellerCreate(email=email, password=password, username=username)
    seller = await SellerService(session=db).add_seller(seller_create=seller_in)
    assert seller.email == email
    assert hasattr(seller, "hashed_password")
