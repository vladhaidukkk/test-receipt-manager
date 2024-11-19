from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.model_types import created_at, intpk

from .base import ModelBase

if TYPE_CHECKING:
    from .payment import PaymentModel
    from .product import ProductModel
    from .user import UserModel


class ReceiptModel(ModelBase):
    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[created_at]

    user: Mapped["UserModel"] = relationship(back_populates="receipts")
    products: Mapped[list["ProductModel"]] = relationship(back_populates="receipt")
    payment: Mapped["PaymentModel"] = relationship(back_populates="receipt")
