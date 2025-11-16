# Minimal FastAPI app to run the resume endpoint

from fastapi import FastAPI
from app.api.v1 import resume as resume_router

app = FastAPI(title="AI Job Recommender - Backend")

app.include_router(resume_router.router)
