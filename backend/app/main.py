# Minimal FastAPI app to run the resume endpoint

from fastapi import FastAPI
from app.api.v1 import resume as resume_router
from app.api.v1 import recommend
from app.api.v1 import skill_gap_simple
from app.api.v1 import learning_path
from app.api.v1 import chat_assistant
app = FastAPI(title="AI Job Recommender - Backend")


app.include_router(resume_router.router)
app.include_router(recommend.router)
app.include_router(skill_gap_simple.router)
app.include_router(learning_path.router)
app.include_router(chat_assistant.router)
