from fastapi import APIRouter
from pydantic import BaseModel

from recommendation_engine.recommendation_engine import generate_recommendations


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


class RecommendationRequest(BaseModel):
    skills: list[str]


@router.post("/")
def get_recommendations(request: RecommendationRequest):
    recommendations = generate_recommendations(request.skills)

    return {
        "success": True,
        "recommendations": recommendations
    }