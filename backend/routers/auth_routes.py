from fastapi import APIRouter, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from backend.core.security import oauth2_scheme

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "fakehashedsecret",
    },
    "alice": {
        "username": "alice",
        "hashed_password": "fakehashedsecret2",
    },
    "ghislain": {
        "username": "ghislain",
        "hashed_password": "fakehashed0000",
    },
}

router = APIRouter(prefix="/auth", tags=["Authentication"])


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


# ----------------------------------------- Start: Methods --------------------------------------


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    # user = fake_decode_token(token)

    print(f"######### {token}#################{get_current_user} ")
    return fake_decode_token(token=token)


async def get_current_user2():

    return "Just for test"


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    print(f"######### {current_user}#################{get_current_active_user} ")
    return current_user


# --------------------------------------------------------- END: MEthods  ----------------------------------------


# 1


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    return {"access_token": "user.username", "token_type": "bearer"}


@router.get("/users/me")
async def read_me(
    current_user: Annotated[str, Depends(get_current_user2)],
):
    return current_user


""" 
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(prefix="/auth")
session = Session(bind=engine)


@auth_router.get("/")
async def hello():
    return {"message": "Hello world"}


@auth_router.post("/signup")
async def signup(user: SignUpModel, status_code=status.HTTP_201_CREATED):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with the email already exists",
        )
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user with the name already exists",
        )
    # new_user = User(**user)
    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()
    return new_user


@auth_router.post("/login")
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username",
        )
    password_ok = check_password_hash(db_user.password, user.password)
    if not password_ok:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Passwords",
        )
    # Everthing is ok...
    access_token = Authorize.create_access_token(subject=db_user.username)
    refresh_token = Authorize.create_refresh_token(subject=db_user.username)

    response = {"access": access_token, "refresh": refresh_token}
    return jsonable_encoder(response)
"""
