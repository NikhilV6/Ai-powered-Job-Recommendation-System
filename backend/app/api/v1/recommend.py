from fastapi import APIRouter
from pydantic import BaseModel

from app.services.vector_index import search_index

router = APIRouter(prefix="/recommend", tags=["Recommendation"])


class Profile(BaseModel):
    text: str


@router.post("/")
def recommend_jobs(profile: Profile):
    return {
        "recommendations": search_index(profile.text)
    }
