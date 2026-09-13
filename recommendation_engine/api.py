from fastapi import APIRouter
from pydantic import BaseModel

from recommendation_engine.recommendation_engine import generate_recommendations


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


class BeneficiaryProfile(BaseModel):
    skills: list[str]
    education: str = ""
    experience: str = ""
    interests: list[str] = []
    location: str = ""
    career_goal: str = ""


@router.post("/")
def get_recommendations(profile: BeneficiaryProfile):

    recommendations = generate_recommendations(
        profile.skills,
        profile.education,
        profile.experience,
        profile.interests
    )

    return {
        "success": True,
        "profile": {
            "education": profile.education,
            "experience": profile.experience,
            "interests": profile.interests,
            "location": profile.location,
            "career_goal": profile.career_goal
        },
        "recommendations": recommendations
    }