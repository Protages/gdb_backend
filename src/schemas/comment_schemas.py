from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    body: str | None = None
    user: int | None = Field(default=None, description='User id')
    game: int | None = Field(default=None, description='Game id')
    review: int | None = Field(default=None, description='Reciew id')


class CommentCreate(CommentBase):
    body: str
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

    class Config:
        orm_mode = True
