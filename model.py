from typing import List

from pydantic import BaseModel


class Repository(BaseModel):
    full_name: str
    clone_url: str


class Organization(BaseModel):
    repositories: List[Repository]
