from fastapi import APIRouter, HTTPException

from backend.schemas.voice import VoiceRequest, VoiceResponse


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


@router.post("/process", response_model=VoiceResponse)
def process_voice(request: VoiceRequest):

    # Check that text is not empty
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )

    # Return the processed Voice AI data
    return VoiceResponse(
        session_id=request.session_id,
        text=request.text,
        language=request.language,
        intent=request.intent,
        skills=request.skills,
        job_domain=request.job_domain,
        entities=request.entities,
        profile=request.profile,
        profile_complete=request.profile_complete,
        next_question=request.next_question
    )