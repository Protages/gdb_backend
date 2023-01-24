import datetime

from pydantic import BaseModel, Field, validator


class GameNested(BaseModel):
    id: int
    title: str | None = None
    main_image_path: str | None = None
    description: str | None = None
    release: datetime.date | None = None
    developer: str | None = None
    production: str | None = None
    system_requirements: str | None = None
    time_to_play: int | None = Field(default=0)

    genres: list | None = []
    platforms: list | None = []

    @validator('genres')
    def genres_validator(cls, v) -> list[int]:
        res = [genre.id for genre in v]
        return res
    
    @validator('platforms')
    def platform_validator(cls, v) -> list[int]:
        res = [platform.id for platform in v]
        return res

    class Config:
        orm_mode = True


class ReviewNested(BaseModel):
    id: int
    author_id: int
    game_id: int
    title: str | None = None
    body: str | None = None
    likes: int | None = Field(default=0)
    rating_minus: int | None = Field(default=0)

    class Config:
        orm_mode = True
