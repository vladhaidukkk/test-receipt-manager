from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.core import inject_session
from app.db.models import UserModel
from app.errors import UserAlreadyExistsError


@inject_session
async def add_user(session: AsyncSession, *, name: str, email: str, password_hash: str) -> UserModel:
    try:
        new_user = UserModel(name=name, email=email, password_hash=password_hash)
        session.add(new_user)
        await session.commit()
    except IntegrityError as error:
        raise UserAlreadyExistsError(email=email) from error
    else:
        return new_user


@inject_session
async def get_user_by_id(session: AsyncSession, *, id_: int) -> UserModel | None:
    query = select(UserModel).filter_by(id=id_)
    return await session.scalar(query)


@inject_session
async def get_user_by_email(session: AsyncSession, *, email: str) -> UserModel | None:
    query = select(UserModel).filter_by(email=email)
    return await session.scalar(query)
