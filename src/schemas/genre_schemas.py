from pydantic import BaseModel


class GenreBase(BaseModel):
    title: str


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class Genre(GenreBase):
    id: int

    class Config:
        orm_mode = True
