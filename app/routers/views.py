from fastapi import APIRouter, Request, status
from fastapi.responses import PlainTextResponse
from fastapi.templating import Jinja2Templates

from app.db.queries import get_receipt_by_id

router = APIRouter(tags=["Views"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/receipts/{receipt_id}")
async def render_receipt(request: Request, receipt_id: int) -> PlainTextResponse:
    receipt = await get_receipt_by_id(id_=receipt_id)

    if receipt:
        template_name = "receipt.txt"
        status_code = status.HTTP_200_OK
    else:
        template_name = "receipt404.txt"
        status_code = status.HTTP_404_NOT_FOUND

    context = {"request": request, "receipt_id": receipt_id, "receipt": receipt}
    content = templates.get_template(template_name).render(context)
    return PlainTextResponse(content, status_code=status_code)
