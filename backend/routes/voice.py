from fastapi import APIRouter, HTTPException

from backend.schemas.voice import VoiceRequest, VoiceResponse
from voice_ai.pipeline.voice_pipeline import VoicePipeline


router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


pipeline = VoicePipeline()


@router.post("/process", response_model=VoiceResponse)
def process_voice(request: VoiceRequest):

    # Check that text is not empty
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty"
        )

    # Process the user's text through Member 3's Voice AI pipeline
    result = pipeline.process_text(
        text=request.text,
        language_code=request.language or "en",
        language_confidence=request.language_confidence or 1.0
    )

    # Return the processed result
    return VoiceResponse(
        session_id=request.session_id,
        text=result["transcription"],
        language=result["language"]["language_code"],
        intent=result["nlp"]["intent"],
        skills=result["nlp"]["skills"],
        job_domain=result["nlp"]["job_domain"],
        entities=result["entities"],
        profile=result["profile"],
        profile_complete=result["profile_complete"],
        next_question=result["next_question"]
    )