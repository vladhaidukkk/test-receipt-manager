from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["Views"])


@router.get("/receipts/{receipt_id}")
async def render_receipt(receipt_id: int) -> PlainTextResponse:
    return PlainTextResponse(f"Receipt ID: {receipt_id}")
