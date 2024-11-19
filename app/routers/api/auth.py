from fastapi import APIRouter, HTTPException, status

from app.db.queries import add_user, get_user_by_email
from app.deps import CurrentUser
from app.errors import UserAlreadyExistsError
from app.models import User, UserCreate, UserLogin, UserRead, UserRegister, UserToken
from app.utils.jwt_utils import create_access_token
from app.utils.password_utils import hash_password, verify_password

router = APIRouter(tags=["Auth API"])


@router.post("/register")
async def register(data: UserRegister) -> UserToken:
    try:
        password_hash = hash_password(data.password)
        user = await add_user(
            data=UserCreate(
                name=data.name,
                email=data.email,
                password_hash=password_hash,
            )
        )
    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered",
        )

    access_token = create_access_token({"sub": str(user.id)})
    return UserToken(access_token=access_token)


@router.post("/login")
async def login(data: UserLogin) -> UserToken:
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
    return UserToken(access_token=access_token)


@router.get("/me", response_model=UserRead)
async def me(current_user: CurrentUser) -> User:
    return current_user
