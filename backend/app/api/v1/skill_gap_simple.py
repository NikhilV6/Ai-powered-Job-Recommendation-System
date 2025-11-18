from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.skill_gap_model import SkillGapModel

router = APIRouter(prefix="/skill-gap-simple", tags=["Skill Gap Simple"])

class Candidate(BaseModel):
    candidate_skills: List[str]

class Job(BaseModel):
    job_id: int
    job_title: str
    skills_required: List[str]
    similarity_score: float

class Req(BaseModel):
    candidate: Candidate
    jobs: List[Job]

@router.post("/")
def analyze(req: Req):
    model = SkillGapModel()
    return model.analyze_multiple(req.candidate.dict(), [j.dict() for j in req.jobs])
