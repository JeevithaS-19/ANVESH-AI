from fastapi import FastAPI
from recommendation_engine.api import router

app = FastAPI(title="ANVESH AI")

app.include_router(router)