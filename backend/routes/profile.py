from fastapi import APIRouter, HTTPException
from backend.schemas.profile import ProfileRequest, ProfileResponse
import uuid


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


profiles = {}


@router.post("/", response_model=ProfileResponse)
def create_profile(profile: ProfileRequest):

    profile_id = str(uuid.uuid4())

    new_profile = ProfileResponse(
        id=profile_id,
        name=profile.name,
        age=profile.age,
        education=profile.education,
        skills=profile.skills
    )

    profiles[profile_id] = new_profile

    return new_profile


@router.get("/{profile_id}", response_model=ProfileResponse)
def get_profile(profile_id: str):

    if profile_id not in profiles:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profiles[profile_id]