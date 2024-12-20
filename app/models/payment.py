from decimal import Decimal
from enum import StrEnum, auto

from pydantic import BaseModel, ConfigDict


class PaymentType(StrEnum):
    CASH = auto()
    CASHLESS = auto()


class PaymentBase(BaseModel):
    type: PaymentType
    amount: Decimal


class Payment(PaymentBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    pass
