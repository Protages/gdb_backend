from pydantic import BaseModel, Field

from src.schemas.game_schemas import GameNested
from src.schemas.user_schemas import UserNested


class CategoryBase(BaseModel):
    title: str | None = None
    games: list[int] | None = Field(default=[], description='Games id')


class CategoryCreate(CategoryBase):
    title: str
    user: int = Field(description='User id')


class CategoryUpdate(CategoryBase):
    pass


class CategoryUpdateGame(BaseModel):
    game: int


class Category(CategoryBase):
    id: int
    user: UserNested
    games: list[GameNested] | None = None

    class Config:
        orm_mode = True
