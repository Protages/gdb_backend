from pydantic import BaseModel, Field

from src.schemas.nested_models import ReviewNested
from src.schemas.user_schemas import UserNested
from src.schemas.game_schemas import GameNested


class ReviewBase(BaseModel):
    title: str | None = None
    body: str | None = None
    likes: int | None = Field(default=0)
    rating_minus: int | None = Field(default=0)
    # comments: list | None = None 


class ReviewCreate(ReviewBase):
    title: str
    author: int = Field(description='User id')
    game: int = Field(description='Game id')
    body: str


class ReviewUpdate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    author: UserNested
    game: GameNested

    class Config:
        orm_mode = True
