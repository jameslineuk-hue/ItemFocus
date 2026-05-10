from typing import Literal

from pydantic import BaseModel, Field

Category = Literal["laptop", "keys", "wallet", "other"]


class CreateTagBody(BaseModel):
    category: Category
    owner_name: str = Field(min_length=1, max_length=200)
    owner_phone: str = Field(min_length=5, max_length=40)


class CreateTagResponse(BaseModel):
    public_code: str
    finder_path: str
    finder_url: str


class FinderResponse(BaseModel):
    public_code: str
    category: Category
    owner_name: str
    owner_phone: str
