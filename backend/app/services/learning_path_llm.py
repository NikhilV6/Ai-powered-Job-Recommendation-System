from typing import List, Dict, Optional
import json
import ast

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings


def get_gemini_llm():
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in .env or environment variables")

    # NOTE: changed from "gemini-1.5-flash" → "gemini-pro"
    # to avoid 404 on older v1beta APIs
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.4,
    )
    return llm


def enrich_learning_path_with_llm(
    base_path: List[Dict],
    candidate_skills: List[str],
    target_skills: List[str],
    job_title: Optional[str] = None,
) -> List[Dict]:
    """
    Use Gemini (via LangChain) to enrich the rule-based plan.
    If anything fails, return base_path unchanged.
    """
    if not base_path:
        return base_path

    try:
        llm = get_gemini_llm()
    except Exception:
        # if key missing or config error → fall back to base_path silently
        return base_path

    prompt_template = ChatPromptTemplate.from_template(
        """
You are a senior software engineering mentor.

Candidate currently knows these skills:
{candidate_skills}

They want to qualify for a job that requires these skills:
{target_skills}

We already prepared a rough week-wise learning path:
{base_path}

Job title (if given): {job_title}

TASK:
Rewrite and ENRICH this learning path:
- Keep the same number of weeks
- For each week, give:
  - week (number)
  - skills (list of skills)
  - goal (1–2 sentences)
  - detailed_plan (3–6 bullet-like strings, but DO NOT use markdown bullets, just plain strings)

Return ONLY valid JSON in this exact structure:
[
  {{
    "week": 1,
    "skills": ["skill1", "skill2"],
    "goal": "short text",
    "detailed_plan": [
      "step 1",
      "step 2"
    ]
  }},
  ...
]
"""
    )

    try:
        chain = prompt_template | llm
        response = chain.invoke(
            {
                "candidate_skills": candidate_skills,
                "target_skills": target_skills,
                "base_path": base_path,
                "job_title": job_title or "Unknown",
            }
        )

        text = response.content

        # Try JSON first
        try:
            enriched = json.loads(text)
        except Exception:
            enriched = ast.literal_eval(text)

        if not isinstance(enriched, list):
            return base_path

        return enriched

    except Exception:
        # any error during LLM call → silently fall back
        return base_path
