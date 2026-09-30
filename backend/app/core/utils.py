from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from .config import settings


# @TODO Must be move to .env
_key = settings.authjwt_secret_key
_algo = settings.authjwt_algorithm


def generate_access_token(data: dict, expiry: timedelta = timedelta(hours=1)):
    # @TODO JWT got 3 parts , head, payloadGenerate Token
    payload = {
        **data,
        "exp": get_datetime_utc() + timedelta(minutes=10),
    }

    tk = jwt.encode(payload=payload, key=_key, algorithm=_algo)
    return tk


def decode_access_token(token: str) -> dict[str, Any]:
    return jwt.decode(jwt=token, key=_key, algorithms=[_algo])


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)
