from pydantic import BaseModel, Field


class OwnerRegisterIn(BaseModel):
    owner_name: str = Field(min_length=2, max_length=255)
    club_name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)


class OwnerLoginIn(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    password: str = Field(min_length=8, max_length=128)
