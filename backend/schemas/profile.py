from pydantic import BaseModel
from typing import Optional


class ProfileRequest(BaseModel):
    name: str
    age: Optional[int] = None
    education: Optional[str] = None
    skills: list[str] = []


class ProfileResponse(BaseModel):
    id: str
    name: str
    age: Optional[int] = None
    education: Optional[str] = None
    skills: list[str] = []