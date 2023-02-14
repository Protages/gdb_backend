from pydantic import BaseModel, Field, validator

from src.schemas.user_schemas import UserNested
from src.schemas.game_schemas import GameNested


class GradeBase(BaseModel):
    score: int

    @validator('score')
    def score_validator(cls, v: int) -> int:
        if v <= 0 or v > 10:
            raise ValueError('Score is not valid, must be from 1 to 10')
        return v


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
