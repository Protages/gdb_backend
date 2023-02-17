from pydantic import BaseModel, Field

from src.schemas.game_schemas import GameNested
from src.schemas.user_schemas import UserNested


class CategoryBase(BaseModel):
    title: str | None = None


class CategoryCreate(CategoryBase):
    title: str
    user: int = Field(description='User id')
    games: list[int] | None = Field(default=[], description='Games id')


class CategoryUpdate(CategoryBase):
    title: str


class CategoryUpdateGame(BaseModel):
    games: list[int]


class Category(CategoryBase):
    id: int
    user: UserNested
    games: list[GameNested] | None = None

    class Config:
        orm_mode = True
