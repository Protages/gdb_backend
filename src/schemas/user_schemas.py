from pydantic import BaseModel, Field

from src.schemas.role_schemas import Role


class UserBase(BaseModel):
    email: str | None = None
    about: str | None = None
    rating: int | None = None


class UserCreate(UserBase):
    email: str
    username: str
    password: str
    is_active: bool | None = Field(default=True)
    is_superuser: bool | None = Field(default=False)


class UserUpdate(UserBase):
    password: str | None = None


class User(UserBase):
    id: int
    username: str
    role: list[Role]
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
