from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.learning_path_service import generate_learning_path

router = APIRouter(prefix="/learning-path", tags=["Learning Path"])


class LearningPathRequest(BaseModel):
    candidate_skills: List[str]
    target_skills: List[str]
    use_llm: bool = False
    job_title: Optional[str] = None


@router.post("/")
def create_learning_path(req: LearningPathRequest):
    result = generate_learning_path(
        candidate_skills=req.candidate_skills,
        target_skills=req.target_skills,
        use_llm=req.use_llm,
        job_title=req.job_title,
    )
    return result
