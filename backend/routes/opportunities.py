from fastapi import APIRouter
from backend.schemas.opportunity import (
    Opportunity,
    OpportunityResponse
)


router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"]
)


@router.get("/", response_model=OpportunityResponse)
def get_opportunities():

    opportunities = [
        Opportunity(
            id="1",
            title="Python Programming Course",
            organization="ANVESH AI",
            type="Course",
            description="Beginner-friendly Python programming course.",
            skills=["Python"],
            link="https://example.com"
        ),
        Opportunity(
            id="2",
            title="Web Development Program",
            organization="ANVESH AI",
            type="Program",
            description="Learn frontend and backend web development.",
            skills=["HTML", "CSS", "JavaScript"],
            link="https://example.com"
        )
    ]

    return OpportunityResponse(
        opportunities=opportunities
    )