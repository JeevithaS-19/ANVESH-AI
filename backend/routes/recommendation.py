from fastapi import APIRouter
from backend.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.post("/", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):

    # Temporary response.
    # Later this will call Member 4's recommendation AI.

    return RecommendationResponse(
        session_id=request.session_id,
        recommended_skills=[],
        recommended_careers=[],
        explanation="Recommendation engine will be connected here."
    )