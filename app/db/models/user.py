from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.model_types import created_at, intpk

from .base import ModelBase

if TYPE_CHECKING:
    from .receipt import ReceiptModel


class UserModel(ModelBase):
    id: Mapped[intpk]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[created_at]

    receipts: Mapped[list["ReceiptModel"]] = relationship(back_populates="user")
