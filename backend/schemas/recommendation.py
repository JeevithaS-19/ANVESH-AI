from pydantic import BaseModel
from typing import Optional


class RecommendationRequest(BaseModel):
    session_id: str
    skills: list[str] = []
    interests: list[str] = []
    education: Optional[str] = None
    career_goal: Optional[str] = None


class RecommendationResponse(BaseModel):
    session_id: str
    recommended_skills: list[str] = []
    recommended_careers: list[str] = []
    explanation: Optional[str] = None