from decimal import Decimal

from pydantic import BaseModel, ConfigDict, computed_field


class ProductBase(BaseModel):
    name: str
    price: Decimal
    quantity: int

    @computed_field
    def total(self) -> Decimal:
        return self.price * self.quantity


class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    pass
