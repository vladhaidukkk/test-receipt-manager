from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.model_types import intpk
from app.models import PaymentType

from .base import ModelBase

if TYPE_CHECKING:
    from .receipt import ReceiptModel


class PaymentModel(ModelBase):
    id: Mapped[intpk]
    type: Mapped[PaymentType]
    amount: Mapped[Decimal]
    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipts.id"))

    receipt: Mapped["ReceiptModel"] = relationship(back_populates="payment")
