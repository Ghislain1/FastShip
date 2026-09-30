# https://fastapi.tiangolo.com/tutorial/security/
# - Security based on username and password
# - OAuth2
# - apiKey
# - http

# Termes:
# - security scheme


# user case: The frontend to authenticate with the backend using a username and password

# AuthJWT (fastapi-jwt-auth) vs. OAuth2PasswordBearer (FastAPI native)
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.seller import Seller
from ..repositories.seller_repository import SellerRepository
from .db import get_async_session
from .utils import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    description="Ghislain Token from Oauth2 Authorize, authorization",
)

_CREDENTIALS_ERROR = "Could not validate credentials"


async def get_current_seller(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Seller:
    """Decode the bearer token and return the authenticated seller."""

    try:
        payload = decode_access_token(token)
        email = payload["user"]["email"]
    except (jwt.PyJWTError, KeyError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_CREDENTIALS_ERROR,
            headers={"WWW-Authenticate": "Bearer"},
        )

    seller = await SellerRepository(session).get_by_email(email)

    if seller is None or not seller.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_CREDENTIALS_ERROR,
            headers={"WWW-Authenticate": "Bearer"},
        )

    return seller


CurrentSellerDep = Annotated[Seller, Depends(get_current_seller)]
