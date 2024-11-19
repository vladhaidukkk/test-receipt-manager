from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, joinedload, selectinload

from app.db.core import inject_session
from app.db.models import PaymentModel, ProductModel, ReceiptModel
from app.models import PaymentType, Receipt, ReceiptCreate


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


@inject_session
async def get_receipts(
    session: AsyncSession, *, user_id: int, payment_type: PaymentType | None = None
) -> list[Receipt]:
    query = (
        select(ReceiptModel)
        .filter_by(user_id=user_id)
        .join(ReceiptModel.products)
        .join(ReceiptModel.payment)
        .options(
            contains_eager(ReceiptModel.products),
            contains_eager(ReceiptModel.payment),
        )
    )
    if payment_type:
        query = query.filter(PaymentModel.type == payment_type)

    receipts = await session.scalars(query)
    return [Receipt.model_validate(receipt) for receipt in receipts.unique()]


@inject_session
async def get_receipt_by_id(session: AsyncSession, *, user_id: int, id_: int) -> Receipt | None:
    query = (
        select(ReceiptModel)
        .filter_by(user_id=user_id, id=id_)
        .options(
            joinedload(ReceiptModel.products),
            selectinload(ReceiptModel.payment),
        )
    )
    receipt = await session.scalar(query)
    return Receipt.model_validate(receipt) if receipt else None
