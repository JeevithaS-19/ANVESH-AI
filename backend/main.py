from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from backend.routes.profile import router as profile_router
from backend.routes.session import router as session_router
from backend.routes.voice import router as voice_router
from backend.routes.recommendation import router as recommendation_router
from backend.routes.opportunities import router as opportunities_router



app = FastAPI(
    title="ANVESH AI API",
    description="Backend API for ANVESH AI",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(session_router)
app.include_router(voice_router)
app.include_router(recommendation_router)
app.include_router(opportunities_router)



@app.get("/")
def root():
    return {
        "message": "ANVESH AI Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }