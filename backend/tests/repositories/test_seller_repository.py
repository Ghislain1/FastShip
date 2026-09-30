from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.seller import Seller
from app.repositories.seller_repository import SellerRepository
from tests.utils.utils import random_email, random_lower_string


async def test_add_and_get_by_email(db: AsyncSession) -> None:
    repository = SellerRepository(db)
    email = random_email()
    seller = Seller(
        email=email,
        name=random_lower_string(),
        hashed_password="hashed",
    )

    added = await repository.add(seller)

    assert added.id is not None
    fetched = await repository.get_by_email(email)
    assert fetched is not None
    assert fetched.id == added.id


async def test_get_by_email_returns_none_when_missing(db: AsyncSession) -> None:
    repository = SellerRepository(db)

    assert await repository.get_by_email(random_email()) is None


async def test_get_by_id_returns_none_when_missing(db: AsyncSession) -> None:
    repository = SellerRepository(db)

    assert await repository.get_by_id(uuid4()) is None


async def test_list_and_count_respect_offset_and_limit(db: AsyncSession) -> None:
    repository = SellerRepository(db)
    for _ in range(3):
        await repository.add(
            Seller(
                email=random_email(),
                name=random_lower_string(),
                hashed_password="hashed",
            )
        )

    assert await repository.count() == 3
    assert len(await repository.list(offset=0, limit=2)) == 2
    assert len(await repository.list(offset=2, limit=10)) == 1
