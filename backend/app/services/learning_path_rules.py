from typing import List, Dict

# Basic priority for skills (you can tune this)
SKILL_PRIORITY = [
    "git",
    "linux",
    "html",
    "css",
    "javascript",
    "typescript",
    "react",
    "redux",
    "node.js",
    "express",
    "python",
    "java",
    "sql",
    "mongodb",
    "postgresql",
    "docker",
    "kubernetes",
    "aws",
    "gcp",
    "azure",
    "ci/cd",
]


def normalize_skill(s: str) -> str:
    return s.strip().lower()


def sort_missing_skills(missing_skills: List[str]) -> List[str]:
    """
    Sort missing skills according to SKILL_PRIORITY.
    Skills not in the list go at the end.
    """
    missing_norm = [normalize_skill(s) for s in missing_skills]
    priority_index = {skill: i for i, skill in enumerate(SKILL_PRIORITY)}

    def sort_key(skill: str):
        return priority_index.get(skill, len(priority_index) + 100)

    return sorted(missing_norm, key=sort_key)


def build_rule_based_learning_path(missing_skills: List[str]) -> List[Dict]:
    """
    Given missing skills, return a week-wise learning plan.

    Output example:
    [
      {
        "week": 1,
        "skills": ["html", "css"],
        "goal": "...",
        "suggested_resources": ["...", "..."]
      },
      ...
    ]
    """
    if not missing_skills:
        return []

    ordered = sort_missing_skills(missing_skills)

    weeks = []
    week_num = 1
    i = 0

    # Simple logic: plan for 1–2 skills per week
    while i < len(ordered):
        chunk = ordered[i:i + 2]

        goal = f"Get comfortable with: {', '.join(chunk)}"
        resources = []
        for skill in chunk:
            resources.append(
                f"Watch 2–3 beginner tutorials on '{skill}', read official docs, "
                f"and build 1 mini project using {skill}."
            )

        weeks.append(
            {
                "week": week_num,
                "skills": chunk,
                "goal": goal,
                "suggested_resources": resources,
            }
        )

        week_num += 1
        i += 2

    return weeks
