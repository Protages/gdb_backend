import datetime

from pydantic import BaseModel, Field

from src.schemas.nested_models import GameNested  # noqa: F401


class GameBase(BaseModel):
    title: str | None = None
    description: str | None = None
    release: datetime.date | None = None
    developer: str | None = None
    production: str | None = None
    system_requirements: str | None = None
    time_to_play: int | None = Field(default=0)
    # comments: list[int] | None = Field(default=[], description='Comments id')
    # grades: list[int] | None = Field(default=[], description='Grades id')


class GameCreate(GameBase):
    title: str
    genres: list[int] = Field(description='Genres id')
    platforms: list[int] = Field(description='Platforms id')
    release: datetime.date


class GameUpdate(GameBase):
    genres: list[int] | None = Field(default=[], description='Genres id')
    platforms: list[int] | None = Field(default=[], description='Platforms id')


class Game(GameBase):
    id: int
    reviews: list | None = []
    genres: list | None = []
    platforms: list | None = []
    comments: list | None = []
    grades: list | None = []

    class Config:
        orm_mode = True
