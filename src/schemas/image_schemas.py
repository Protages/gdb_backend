from pydantic import BaseModel, Field, validator


class Image(BaseModel):
    image_path: str

    class Config:
        orm_mode = True
