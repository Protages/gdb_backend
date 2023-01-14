from pydantic import BaseModel, Field


class GradeBase(BaseModel):
    score: int | None = None
    user: int | None = None
    game: int | None = None


class GradeCreate(GradeBase):
    score: int
    user: int = Field(description='User id')
    game: int = Field(description='Game id')


class GradeUpdate(GradeBase):
    pass


class Grade(GradeBase):
    id: int

    class Config:
        orm_mode = True
