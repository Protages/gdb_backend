from pydantic import BaseModel, validator, Field

from src.schemas.role_schemas import Role
from src.api_v1.validators import (
    email_validator, 
    username_validator,
    password_validator
)
from src.schemas.token_schemas import Token


class UserBase(BaseModel):
    about: str | None = None
    rating: int | None = None
    is_active: bool | None = Field(default=True)
    is_superuser: bool | None = Field(default=False)


class UserCreate(UserBase):
    email: str = Field(example='example@gmail.com')
    username: str
    password: str
    roles: list[int] | None = Field(default=[], description='Roles id')

    @validator('email')
    def email_valid(cls, v: str) -> str:
        if not email_validator(v):
            raise ValueError('Email is not valid')
        return v

    @validator('username')
    def username_valid(cls, v: str) -> str:
        if not username_validator(v):
            raise ValueError('Username is not valid')
        return v

    @validator('password')
    def password_valid(cls, v: str) -> str:
        if not password_validator(v):
            raise ValueError('Password is not valid')
        return v


class UserUpdate(UserBase):
    password: str | None = None
    roles: list[int] | None = Field(default=[], description='Roles id')

    @validator('password')
    def password_valid(cls, v: str) -> str:
        if not password_validator(v):
            raise ValueError('Password is not valid')
        return v


class User(UserBase):
    id: int
    username: str
    email: str
    is_email_confirmed: bool | None
    roles: list[Role] | None = []

    class Config:
        orm_mode = True


class UserNested(UserBase):
    id: int
    username: str
    email: str
    is_email_confirmed: bool
    roles: list | None = []

    @validator('roles')
    def roles_validator(cls, v: list[int]) -> list[int]:
        res = [role.id for role in v]
        return res

    class Config:
        orm_mode = True


class UserAndToken(BaseModel):
    user: User
    token: Token

    class Config:
        orm_mode = True
