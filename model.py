from typing import List

from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    full_name: str
    clone_url: str
    language: str


class Organization(BaseModel):
    name: str
    repositories: List[Repository]
