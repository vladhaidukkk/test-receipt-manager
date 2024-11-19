from decimal import Decimal

from pydantic import BaseModel, ConfigDict, computed_field


class ProductBase(BaseModel):
    name: str
    price: Decimal
    quantity: int


class Product(ProductBase):
    id: int

    @computed_field
    def total(self) -> Decimal:
        return self.price * self.quantity

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    @computed_field
    def total(self) -> Decimal:
        return self.price * self.quantity
