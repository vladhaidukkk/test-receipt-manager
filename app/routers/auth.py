from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["Auth"])


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


@router.post("/register")
async def register(data: UserRegister) -> dict:
    return {"message": "Register"}


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(data: UserLogin) -> dict:
    return {"message": "Login"}
