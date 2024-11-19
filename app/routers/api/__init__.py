from fastapi import APIRouter

from .auth import router as auth_router
from .receipts import router as receipts_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth")
router.include_router(receipts_router, prefix="/receipts")
