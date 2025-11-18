# Minimal FastAPI app to run the resume endpoint

from fastapi import FastAPI
from app.api.v1 import resume as resume_router
from app.api.v1 import recommend
from app.api.v1 import skill_gap_simple
app = FastAPI(title="AI Job Recommender - Backend")

app.include_router(skill_gap_simple.router)

app.include_router(resume_router.router)


app.include_router(recommend.router)
