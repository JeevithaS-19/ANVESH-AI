
from fastapi import APIRouter

from backend.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse
)

from recommendation_engine.recommendation_engine import generate_recommendations

from backend.knowledge_base.adapter import (
    get_opportunities_for_occupation,
    get_nsqf_training_for_occupation
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"]
)


@router.post("/", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):

    # ------------------------------------------------
    # Get profile data from Member 1 frontend
    # ------------------------------------------------

    profile = request.profile or {}

    # Support both:
    # 1. Member 1 format: data inside "profile"
    # 2. Direct backend format: skills, education, etc.
    skills = request.skills or profile.get("skills", [])

    education = request.education or profile.get("education", "")

    # Member 1 sends education as a list
    if isinstance(education, list):
        education = ", ".join(str(item) for item in education)

    experience = request.experience or profile.get("experience", "")

    interests = request.interests or profile.get("interests", [])

    location = request.location or profile.get("location", "")

    # Member 1 uses job_domain instead of career_goal
    career_goal = (
        request.career_goal
        or profile.get("career_goal")
        or profile.get("job_domain")
        or profile.get("intent")
        or ""
    )

    # ------------------------------------------------
    # Generate recommendations
    # ------------------------------------------------

    results = generate_recommendations(
        skills,
        education,
        experience,
        interests,
        career_goal
    )

    # ------------------------------------------------
    # If recommendation engine returns nothing
    # ------------------------------------------------

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
    # NSQF pathway from Member 5 knowledge base
    # ------------------------------------------------

    occupation_name = best.get("occupation", "")

    knowledge_base_training = get_nsqf_training_for_occupation(
        occupation_name
    )

    nsqf_pathway = []

    for item in knowledge_base_training:
        nsqf_pathway.append({
            "level": item.get("level", ""),
            "title": item.get("title", ""),
            "meta": (
                f"Provider: {item.get('provider', '')}; "
                f"Mode: {item.get('mode', '')}; "
                f"Duration: {item.get('duration_weeks', '')} weeks"
            )
        })

    # ------------------------------------------------
    # Opportunities from Member 5 knowledge base
    # ------------------------------------------------

    knowledge_base_opportunities = get_opportunities_for_occupation(
        occupation_name
    )

    opportunities = []

    for item in knowledge_base_opportunities:
        opportunities.append({
            "id": item.get("opportunity_id", ""),
            "title": item.get("title", ""),
            "organization": "",
            "type": item.get("type", ""),
            "description": f"Location: {item.get('location', '')}",
            "skills": matched_skills,
            "link": ""
        })

    return RecommendationResponse(
        session_id=request.session_id,
        skillGap=skill_gap,
        nsqf_pathway=nsqf_pathway,
        recommendation=recommendation,
        opportunities=opportunities
    )

