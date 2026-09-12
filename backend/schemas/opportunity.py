from pydantic import BaseModel
from typing import Optional


class Opportunity(BaseModel):
    id: str
    title: str
    organization: Optional[str] = None
    type: str
    description: Optional[str] = None
    skills: list[str] = []
    link: Optional[str] = None


class OpportunityResponse(BaseModel):
    opportunities: list[Opportunity]