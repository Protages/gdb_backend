from pydantic import BaseModel


class PlatformBase(BaseModel):
    title: str


class PlatformCreate(PlatformBase):
    pass


class PlatformUpdate(PlatformBase):
    pass


class Platform(PlatformBase):
    id: int

    class Config:
        orm_mode = True
