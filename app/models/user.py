from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class User(UserBase):
    id: int
    password_hash: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBase):
    password_hash: str


class UserRead(UserBase):
    id: int
