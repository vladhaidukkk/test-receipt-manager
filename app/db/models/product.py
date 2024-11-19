from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.model_types import intpk

from .base import ModelBase

if TYPE_CHECKING:
    from .receipt import ReceiptModel


class ProductModel(ModelBase):
    id: Mapped[intpk]
    name: Mapped[str]
    price: Mapped[Decimal]
    quantity: Mapped[int]
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))

    receipt: Mapped["ReceiptModel"] = relationship(back_populates="products")
