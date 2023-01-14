from pydantic import BaseModel, Field

from src.schemas.game_schemas import Game


class CategoryBase(BaseModel):
    title: str | None = None
    user: int | None = Field(default=None, description='User id')
    games: list[int] | None = Field(default=None, description='Games id')


class CategoryCreate(CategoryBase):
    title: str
    user: int = Field(description='User id')


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    games: list[Game] | None = None

    class Config:
        orm_mode = True
