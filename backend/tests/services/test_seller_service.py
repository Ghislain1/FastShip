import pytest
from app.schemas.seller import SellerCreate
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.seller_service import SellerService
from tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_create_seller(db: AsyncSession) -> None:
    email = random_email()
    password = random_lower_string()
    name = random_lower_string()
    seller_in = SellerCreate(email=email, password=password, name=name)
    seller = await SellerService(session=db).add_seller(seller_create=seller_in)
    assert seller.email == email
    assert hasattr(seller, "hashed_password")


@pytest.mark.asyncio
async def test_created_seller_is_not_a_superuser(db: AsyncSession) -> None:
    seller_in = SellerCreate(
        email=random_email(), password=random_lower_string(), name=random_lower_string()
    )
    seller = await SellerService(session=db).add_seller(seller_create=seller_in)
    assert seller.is_superuser is False


@pytest.mark.asyncio
async def test_add_seller_can_grant_superuser_internally(db: AsyncSession) -> None:
    """The seeder path must still be able to create an admin.

    `is_superuser` is keyword-only and absent from SellerCreate, so this is the
    only way to set it.
    """
    seller_in = SellerCreate(
        email=random_email(), password=random_lower_string(), name=random_lower_string()
    )
    seller = await SellerService(session=db).add_seller(
        seller_create=seller_in, is_superuser=True
    )
    assert seller.is_superuser is True
