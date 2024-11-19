from fastapi import APIRouter

from app.db.queries import add_receipt
from app.deps import CurrentUser
from app.models import Receipt, ReceiptCreate, ReceiptRead

router = APIRouter(tags=["Receipts"])


@router.post("", response_model=ReceiptRead)
async def create_receipt(current_user: CurrentUser, data: ReceiptCreate) -> Receipt:
    return await add_receipt(user_id=current_user.id, data=data)
