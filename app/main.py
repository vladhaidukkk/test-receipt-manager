from fastapi import FastAPI

from app.routers import api_router, views_router

app = FastAPI()

app.include_router(api_router, prefix="/api")
app.include_router(views_router)
