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
