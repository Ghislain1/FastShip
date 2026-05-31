from datetime import datetime, timedelta, timezone

import jwt


# @TODO Must be move to .env
_key = "ANY_KEY_GHISLAIN"
_algo = "HS256"


def generate_access_token(data: dict, expiry: timedelta = timedelta(hours=1)):
    # @TODO JWT got 3 parts , head, payloadGenerate Token
    payload = {
        **data,
        "exp": get_datetime_utc() + timedelta(minutes=10),
    }

    tk = jwt.encode(payload=payload, key=_key, algorithm=_algo)
    return tk


def decode_access_token(token: str) -> dict[str, any]:
    return jwt.decode(jwt=token, key=_key, algorithms=[_algo])


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)
