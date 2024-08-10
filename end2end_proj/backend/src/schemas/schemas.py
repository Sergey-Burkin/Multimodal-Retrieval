from pydantic import BaseModel
from src.models import models


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    # email: str = "example@mail.ru"
    username: str = "example"
    # full_name: str | None = "full name example"


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    # disabled: bool = False
    hashed_password: str
    # items: list[Item] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def make_schema_user(user: models.User) -> User:
    return User(
        # email=user.email,
        username=user.username,
        # full_name=user.full_name,
        id=user.id,
        # disabled=user.disabled,
        hashed_password=user.hashed_password,
        items=user.items,
    )
