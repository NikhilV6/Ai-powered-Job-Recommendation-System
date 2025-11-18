from typing import List, Dict, Optional

from app.services.learning_path_rules import build_rule_based_learning_path, normalize_skill
from app.services.learning_path_llm import enrich_learning_path_with_llm


def generate_learning_path(
    candidate_skills: List[str],
    target_skills: List[str],
    use_llm: bool = False,
    job_title: Optional[str] = None,
) -> Dict:
    """
    - Computes missing skills
    - Builds rule-based path
    - Optionally enriches with Gemini (LLM)
    """

    cand_set = {normalize_skill(s) for s in candidate_skills}
    target_set = {normalize_skill(s) for s in target_skills}

    missing = sorted(list(target_set - cand_set))

    base_path = build_rule_based_learning_path(missing)

    final_path = base_path
    if use_llm and base_path:
        final_path = enrich_learning_path_with_llm(
            base_path=base_path,
            candidate_skills=sorted(list(cand_set)),
            target_skills=sorted(list(target_set)),
            job_title=job_title,
        )

    return {
        "candidate_skills": sorted(list(cand_set)),
        "target_skills": sorted(list(target_set)),
        "missing_skills": missing,
        "plan": final_path,
    }
