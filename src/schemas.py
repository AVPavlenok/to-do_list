from pydantic import BaseModel, Field


class TaskIn(BaseModel):
    task: str


class TaskOut(BaseModel):
    id: int
    task: str
    is_complete: bool

    class Config:
        from_attributes = True


class TaskChange(BaseModel):
    id: int
    is_complete: bool


class UserBase(BaseModel):
    login: str = Field(
        ...,
        min_length=5
    )
    password: str = Field(
        ...,
        min_length=8
    )


class UserPublic(BaseModel):
    name: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    name: str


