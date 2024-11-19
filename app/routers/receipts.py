import datetime as dt

from fastapi import APIRouter, HTTPException, status

from app.db.queries import add_receipt, get_receipt_by_id, get_receipts
from app.deps import CurrentUser
from app.models import PaymentType, Receipt, ReceiptCreate, ReceiptRead

router = APIRouter(tags=["Receipts"])


@router.post("", response_model=ReceiptRead)
async def create_receipt(current_user: CurrentUser, data: ReceiptCreate) -> Receipt:
    return await add_receipt(user_id=current_user.id, data=data)


@router.get("", response_model=list[ReceiptRead])
async def read_receipts(
    current_user: CurrentUser,
    date_from: dt.datetime | None = None,
    min_total: int | None = None,
    payment_type: PaymentType | None = None,
    offset: int | None = None,
) -> list[Receipt]:
    return await get_receipts(
        user_id=current_user.id,
        date_from=date_from,
        min_total=min_total,
        payment_type=payment_type,
        offset=offset,
    )


@router.get("/{receipt_id}", response_model=ReceiptRead)
async def read_receipt(current_user: CurrentUser, receipt_id: int) -> Receipt:
    receipt = await get_receipt_by_id(user_id=current_user.id, id_=receipt_id)
    if not receipt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Receipt not found",
        )
    return receipt
