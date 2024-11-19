from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.db.queries import add_user, get_user_by_email
from app.deps import get_current_user
from app.errors import UserAlreadyExistsError
from app.models import User
from app.utils.jwt_utils import create_access_token
from app.utils.password_utils import hash_password, verify_password

router = APIRouter(tags=["Auth"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


@router.post("/register")
async def register(data: UserRegister) -> Token:
    try:
        password_hash = hash_password(data.password)
        user = await add_user(
            name=data.name,
            email=data.email,
            password_hash=password_hash,
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered",
        )

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(data: UserLogin) -> Token:
    validation_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )

    user = await get_user_by_email(email=data.email)
    if not user:
        raise validation_error

    if not verify_password(data.password, user.password_hash):
        raise validation_error

    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get("/me")
async def me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user
