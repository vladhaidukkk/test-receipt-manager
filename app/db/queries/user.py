from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.core import inject_session
from app.db.models import UserModel
from app.errors import UserAlreadyExistsError
from app.models import User, UserCreate


@inject_session
async def add_user(session: AsyncSession, *, data: UserCreate) -> User:
    try:
        new_user = UserModel(name=data.name, email=data.email, password_hash=data.password_hash)
        session.add(new_user)
        await session.commit()
    except IntegrityError as error:
        raise UserAlreadyExistsError(email=data.email) from error
    else:
        return User.model_validate(new_user)


@inject_session
async def get_user_by_id(session: AsyncSession, *, id_: int) -> User | None:
    query = select(UserModel).filter_by(id=id_)
    user = await session.scalar(query)
    return User.model_validate(user) if user else None


@inject_session
async def get_user_by_email(session: AsyncSession, *, email: str) -> User | None:
    query = select(UserModel).filter_by(email=email)
    user = await session.scalar(query)
    return User.model_validate(user) if user else None
