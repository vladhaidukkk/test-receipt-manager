from sqlalchemy.orm import Mapped, mapped_column

from app.db.model_types import created_at, intpk

from .base import ModelBase


class UserModel(ModelBase):
    id: Mapped[intpk]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[created_at]
