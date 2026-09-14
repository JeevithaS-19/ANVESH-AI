from pydantic import BaseModel
from typing import Optional


class RecommendationRequest(BaseModel):
    session_id: str

    # Profile data coming from Member 1 frontend
    skills: list[str] = []
    interests: list[str] = []

    education: Optional[str] = None
    experience: Optional[str] = None
    location: Optional[str] = None
    career_goal: Optional[str] = None


class RecommendationResponse(BaseModel):
    session_id: str

    # Data required by Member 1 frontend
    skillGap: dict = {}
    nsqf_pathway: list[dict] = []
    recommendation: dict = {}
    opportunities: list[dict] = []