import datetime as dt
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, computed_field

from .payment import Payment, PaymentCreate, PaymentRead
from .product import Product, ProductCreate, ProductRead


class ReceiptBase(BaseModel):
    @computed_field
    def total(self) -> Decimal:
        return sum([product.total for product in self.products])

    @computed_field
    def rest(self) -> Decimal:
        return self.payment.amount - self.total


class Receipt(ReceiptBase):
    id: int
    products: list[Product]
    payment: Payment
    created_at: dt.datetime

    model_config = ConfigDict(from_attributes=True)


class ReceiptCreate(ReceiptBase):
    products: list[ProductCreate]
    payment: PaymentCreate


class ReceiptRead(Receipt):
    id: int
    products: list[ProductRead]
    payment: PaymentRead
    created_at: dt.datetime
