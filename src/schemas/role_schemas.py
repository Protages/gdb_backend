from pydantic import BaseModel


class RoleBase(BaseModel):
    title: str | None = None


class RoleCreate(RoleBase):
    title: str


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True
