from datetime import datetime, timedelta

import jwt

from backend.models.customer import Customer

# @TODO Must be move to .env
_key = "ANY_KEY_GHISLAIN"
_algo = "HS256"


def generate_access_token(data: dict, expiry: timedelta = timedelta(hours=1)):
    # @TODO JWT got 3 parts , head, payloadGenerate Token
    payload = {
        **data,
        "exp": datetime.now() + timedelta(minutes=10),
    }

    tk = jwt.encode(payload=payload, key=_key, algorithm=_algo)
    return tk


def generate_access_token2(customer: Customer, expiry: timedelta = timedelta(hours=1)):
    # @TODO JWT got 3 parts , header, payload ,Algo
    payload = {
        "user": {
            "name": customer.username,
            "email": customer.email,
        },
        "exp": datetime.now() + timedelta(minutes=10),
    }
    # @TODO Must be move to .env
    algo = "HS256"
    key = "ANY_KEY_GHISLAIN"

    tk = jwt.encode(payload=payload, key=key, algorithm=algo)
    return tk


def decode_access_token(token: str) -> dict[str, any]:
    return jwt.decode(jwt=token, key=_key, algorithms=[_algo])
