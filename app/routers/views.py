from fastapi import APIRouter, Request, status
from fastapi.responses import PlainTextResponse

from app.db.queries import get_receipt_by_id
from app.utils.format_utils import ReceiptFormatter

router = APIRouter(tags=["Views"])


@router.get("/receipts/{receipt_id}")
async def render_receipt(request: Request, receipt_id: int) -> PlainTextResponse:
    receipt = await get_receipt_by_id(id_=receipt_id)

    if receipt:
        content = ReceiptFormatter(width=33).format(receipt)
        status_code = status.HTTP_200_OK
    else:
        content = f"Receipt {receipt_id} not found"
        status_code = status.HTTP_404_NOT_FOUND

    return PlainTextResponse(content, status_code=status_code)
