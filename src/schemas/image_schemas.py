from pydantic import BaseModel


class Image(BaseModel):
    image_path: str

    class Config:
        orm_mode = True
