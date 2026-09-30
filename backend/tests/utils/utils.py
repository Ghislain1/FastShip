import random
import string

from app.core.utils import generate_access_token


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_password() -> str:
    return random_lower_string()[:12]


def auth_headers(
    email: str, seller_id: str = "00000000-0000-0000-0000-000000000000"
) -> dict:
    """Build a valid Authorization header without a login round-trip."""
    token = generate_access_token(
        {"user": {"name": "Test", "email": email, "id": seller_id}}
    )
    return {"Authorization": f"Bearer {token}"}
