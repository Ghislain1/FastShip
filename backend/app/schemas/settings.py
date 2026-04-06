from pydantic import BaseModel


class Settings(BaseModel):
    """Import must start with authjwt_"""

    authjwt_secret_key: str = (
        "b223e6d3a9a3ec3f00c38f7ad5f9344c22fde8f11edb85caf41623d8f27de345"
    )
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 100  # seconds
