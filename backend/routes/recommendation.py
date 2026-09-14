from fastapi import APIRouter

from backend.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse
)

from recommendation_engine.recommendation_engine import generate_recommendations


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.post("/", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):

    results = generate_recommendations(
        request.skills,
        request.education or "",
        request.experience or "",
        request.interests,
        request.career_goal or ""
    )

    # If recommendation engine returns nothing
    if not results:
        return RecommendationResponse(
            session_id=request.session_id,
            skillGap={
                "matched_skills": [],
                "missing_skills": [],
                "gap_percent": 100
            },
            nsqf_pathway=[],
            recommendation={},
            opportunities=[]
        )

    # ------------------------------------------------
    # Best recommendation = first ranked result
    # ------------------------------------------------

    best = results[0]

    matched_skills = best.get("matched_skills", [])
    missing_skills = best.get("missing_skills", [])

    total_skills = len(matched_skills) + len(missing_skills)

    if total_skills > 0:
        gap_percent = round(
            (len(missing_skills) / total_skills) * 100
        )
    else:
        gap_percent = 0

    # ------------------------------------------------
    # Skill gap
    # ------------------------------------------------

    skill_gap = {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "gap_percent": gap_percent
    }

    # ------------------------------------------------
    # Best occupation recommendation
    # ------------------------------------------------

    recommendation = {
        "occupation": best.get("occupation", ""),
        "compatibility_score": best.get("compatibility_score", 0),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "explanation": best.get("explanation", "")
    }

    # ------------------------------------------------
    # Training / NSQF pathway
    # ------------------------------------------------

    nsqf_pathway = []

    training = best.get("training", [])

    if isinstance(training, list):

        for item in training:

            if isinstance(item, dict):

                nsqf_pathway.append({
                    "level": item.get("level", ""),
                    "title": item.get(
                        "title",
                        item.get("name", "")
                    ),
                    "meta": item.get(
                        "meta",
                        item.get("description", "")
                    )
                })

            else:

                nsqf_pathway.append({
                    "level": "",
                    "title": str(item),
                    "meta": ""
                })

    # ------------------------------------------------
    # Opportunities will be connected separately
    # with Member 5's knowledge base.
    # ------------------------------------------------

    opportunities = []

    return RecommendationResponse(
        session_id=request.session_id,
        skillGap=skill_gap,
        nsqf_pathway=nsqf_pathway,
        recommendation=recommendation,
        opportunities=opportunities
    )