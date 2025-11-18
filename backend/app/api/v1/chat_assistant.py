from typing import Optional, List, Dict, Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_assistant import chat_career_assistant

router = APIRouter(prefix="/chat", tags=["Career Chat Assistant"])


# ---------- Pydantic Models for JSON Answer ----------

class CareerOption(BaseModel):
    role: str
    core_skills: List[str]
    why_suitable: str
    next_steps: List[str]


class AnswerJSON(BaseModel):
    answer_summary: str
    career_options: List[CareerOption] = []
    guidance: List[str] = []


# ---------- Request / Response Models ----------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    top_k: int = 5

    # Learning path options
    generate_learning_path: bool = False
    candidate_skills: Optional[List[str]] = None
    target_skills: Optional[List[str]] = None
    job_title: Optional[str] = None


class ChatResponse(BaseModel):
    session_id: str
    answer: AnswerJSON
    used_top_k: int
    learning_path: Optional[Dict[str, Any]] = None


@router.post("/", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = chat_career_assistant(
        message=req.message,
        session_id=req.session_id,
        top_k=req.top_k,
        generate_learning_path_flag=req.generate_learning_path,
        candidate_skills=req.candidate_skills,
        target_skills=req.target_skills,
        job_title=req.job_title,
    )

    return ChatResponse(
        session_id=result["session_id"],
        answer=result["answer_json"],
        used_top_k=result["used_top_k"],
        learning_path=result["learning_path"],
    )
