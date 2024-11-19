from typing import Annotated

from fastapi import Header, HTTPException, status
from jwt import InvalidTokenError

from app.db.queries import get_user_by_id
from app.models import User
from app.utils.jwt_utils import decode_access_token


async def get_current_user(bearer_token: Annotated[str, Header(alias="Authorization-Token")]) -> User:
    creds_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        _, token = bearer_token.split()
        payload = decode_access_token(token)
    except (InvalidTokenError, ValueError):
        raise creds_error

    user_id = payload.get("sub")
    if not user_id:
        raise creds_error

    user = await get_user_by_id(id_=int(user_id))
    if not user:
        raise creds_error

    return User(id=user.id, name=user.name, email=user.email)
