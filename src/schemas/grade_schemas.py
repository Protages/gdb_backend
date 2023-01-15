from pydantic import BaseModel, Field

from src.schemas.user_schemas import UserNested
from src.schemas.game_schemas import GameNested


class GradeBase(BaseModel):
    score: int


class GradeCreate(GradeBase):
    user: int = Field(description='User id')
    game: int = Field(description='Game id')


class GradeUpdate(GradeBase):
    pass


class Grade(GradeBase):
    id: int
    user: UserNested
    game: GameNested

    class Config:
        orm_mode = True
