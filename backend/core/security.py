# https://fastapi.tiangolo.com/tutorial/security/
# - Security based on username and password
# - OAuth2
# - apiKey
# - http

# Termes:
# - security scheme


# user case: The frontend to authenticate with the backend using a username and password

# AuthJWT (fastapi-jwt-auth) vs. OAuth2PasswordBearer (FastAPI native)
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token",
    description="Ghislain Token from Oauth2 Authorize, authorization",
)
