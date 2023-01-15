from pydantic import BaseModel, Field

from src.schemas.user_schemas import UserNested
from src.schemas.game_schemas import GameNested
from src.schemas.review_schemas import ReviewNested


class CommentBase(BaseModel):
    body: str


class CommentCreate(CommentBase):
    user: int
    game: int | None = Field(
        default=None, description='Need to pass game or review id'
    )
    review: int | None = Field(
        default=None, description='Need to pass game or review id'
    )


class CommentUpdate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    user: UserNested
    game: GameNested | None = None
    review: ReviewNested | None = None

    class Config:
        orm_mode = True
