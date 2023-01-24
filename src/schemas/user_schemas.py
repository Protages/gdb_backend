from pydantic import BaseModel, validator, Field

from src.schemas.role_schemas import Role
from src.api_v1.validators import email_validator
from src.schemas.token_schemas import Token


class UserBase(BaseModel):
    email: str | None = Field(default=None, example='example@gmail.com')
    about: str | None = None
    rating: int | None = None
    is_active: bool | None = Field(default=True)
    is_superuser: bool | None = Field(default=False)

    @validator('email')
    def email_valid(cls, v):
        if not email_validator(v):
            raise ValueError('Email is not valid')
        return v


class UserCreate(UserBase):
    email: str = Field(example='example@gmail.com')
    username: str
    password: str
    roles: list[int] | None = Field(default=[], description='Roles id')


class UserUpdate(UserBase):
    password: str | None = None
    roles: list[int] | None = Field(default=[], description='Roles id')


class User(UserBase):
    id: int
    username: str
    roles: list[Role] | None = []

    class Config:
        orm_mode = True


class UserNested(UserBase):
    id: int
    username: str
    roles: list | None = []

    @validator('roles')
    def roles_validator(cls, v) -> list[int]:
        res = [role.id for role in v]
        return res

    class Config:
        orm_mode = True


class UserAndToken(BaseModel):
    user: User
    token: Token

    class Config:
        orm_mode = True
