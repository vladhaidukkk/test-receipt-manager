import datetime as dt
from decimal import Decimal

from sqlalchemy import func, select
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
    filtered_receipts_query = (
        select(ReceiptModel.id.label("receipt_id"))
        .join(ReceiptModel.products)
        .join(ReceiptModel.payment)
        .filter(ReceiptModel.user_id == user_id)
        .group_by(ReceiptModel.id)
    )

    if date_from:
        filtered_receipts_query = filtered_receipts_query.filter(ReceiptModel.created_at >= date_from)
    if min_total:
        filtered_receipts_query = filtered_receipts_query.having(
            func.sum(ProductModel.price * ProductModel.quantity) >= min_total
        )
    if payment_type:
        filtered_receipts_query = filtered_receipts_query.filter(PaymentModel.type == payment_type)

    filtered_receipts_cte = filtered_receipts_query.cte("filtered_receipts")
    query = (
        select(ReceiptModel)
        .join(filtered_receipts_cte, ReceiptModel.id == filtered_receipts_cte.c.receipt_id)
        .options(
            joinedload(ReceiptModel.products),
            selectinload(ReceiptModel.payment),
        )
        .order_by(ReceiptModel.created_at.desc())
    )

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
