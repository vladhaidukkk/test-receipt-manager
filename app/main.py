from fastapi import FastAPI

from app.routers import auth_router, receipts_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth")
app.include_router(receipts_router, prefix="/receipts")
