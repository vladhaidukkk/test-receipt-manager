from sqlalchemy.ext.asyncio import AsyncSession

from app.db.core import inject_session
from app.db.models import PaymentModel, ProductModel, ReceiptModel
from app.models import Receipt, ReceiptCreate


@inject_session
async def add_receipt(session: AsyncSession, *, user_id: int, data: ReceiptCreate) -> Receipt:
    new_products = [
        ProductModel(name=product.name, price=product.price, quantity=product.quantity) for product in data.products
    ]
    new_payment = PaymentModel(type=data.payment.type, amount=data.payment.amount)
    new_receipt = ReceiptModel(user_id=user_id, products=new_products, payment=new_payment)

    session.add(new_receipt)
    await session.commit()

    return Receipt.model_validate(new_receipt)
