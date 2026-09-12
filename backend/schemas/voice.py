from pydantic import BaseModel
from typing import Optional


class VoiceRequest(BaseModel):
    session_id: str
    text: str

    language: Optional[str] = None
    language_confidence: Optional[float] = None

    intent: Optional[str] = None
    skills: list[str] = []
    job_domain: Optional[str] = None

    entities: dict = {}

    profile: dict = {}

    profile_complete: bool = False
    next_question: Optional[str] = None


class VoiceResponse(BaseModel):
    session_id: str
    text: str

    language: Optional[str] = None
    intent: Optional[str] = None
    skills: list[str] = []
    job_domain: Optional[str] = None

    entities: dict = {}

    profile: dict = {}

    profile_complete: bool = False
    next_question: Optional[str] = None