import datetime as dt

import jwt

from app.config import settings


def create_access_token(data: dict[str, str]) -> str:
    expire = dt.datetime.now(dt.UTC) + dt.timedelta(minutes=settings.jwt.access_token_expire_minutes)
    payload = {**data, "exp": expire}
    return jwt.encode(payload, key=settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, key=settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
