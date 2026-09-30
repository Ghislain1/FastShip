# POSTGRES_URL = "postgresql://postgres:namej345@localhost/pizza_deliver_db"
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# postgresql+psycopg://user:password@localhost/dbname
DATABASE_FOR_DOCKER = (
    "postgresql+asyncio://postgres:fastship123@localhost:5432/fastship"
)
# aiosqlite
DATABASE_FOR_LOCAL = "sqlite+aiosqlite:///fastship.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    DATABASE_URL: str = DATABASE_FOR_LOCAL
    FIRST_SUPERUSER: EmailStr = "admin@admin.de"
    FIRST_SUPERUSER_PASSWORD: str = "admin"
    FIRST_SUPERUSER_NAME: str = "Admin"
    authjwt_secret_key: str = (
        "b223e6d3a9a3ec3f00c38f7ad5f9344c22fde8f11edb85caf41623d8f27de345"
    )
    authjwt_algorithm: str = "HS256"
    authjwt_access_token_expires: int = 100  # seconds

    # Dev only: inserts fake shipments/orders on startup. Opt in with
    # MOCK_SEED=true. Keep it off in any deployed environment.
    MOCK_SEED: bool = False


# One Instance of Setting
settings = Settings()
