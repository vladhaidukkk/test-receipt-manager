import datetime as dt
from decimal import Decimal

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
    session: AsyncSession,
    *,
    user_id: int,
    date_from: dt.datetime | None = None,
    min_total: Decimal | None = None,
    payment_type: PaymentType | None = None,
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
    if date_from:
        query = query.filter(ReceiptModel.created_at >= date_from)
    if payment_type:
        query = query.filter(PaymentModel.type == payment_type)

    receipts = await session.scalars(query)
    receipts = [Receipt.model_validate(receipt) for receipt in receipts.unique()]

    # This can be optimized by adding a filter in the query itself.
    if min_total:
        receipts = [receipt for receipt in receipts if receipt.total >= min_total]

    return receipts


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
