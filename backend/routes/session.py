from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid


router = APIRouter(
    prefix="/session",
    tags=["Session"]
)


class SessionRequest(BaseModel):
    profile_id: str


class SessionResponse(BaseModel):
    session_id: str
    profile_id: str


sessions = {}


@router.post("/", response_model=SessionResponse)
def create_session(request: SessionRequest):

    session_id = str(uuid.uuid4())

    sessions[session_id] = request.profile_id

    return SessionResponse(
        session_id=session_id,
        profile_id=request.profile_id
    )


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(session_id: str):

    if session_id not in sessions:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return SessionResponse(
        session_id=session_id,
        profile_id=sessions[session_id]
    )