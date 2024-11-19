from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: str


class UserToken(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    name: str
    email: EmailStr
    password: str
