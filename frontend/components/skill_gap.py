import streamlit as st
from api_client import run_skill_gap



def extract_job_title(job_text):
    """Extract the first 2 words as job title."""
    words = job_text.split()
    return " ".join(words[:2])  # simple heuristic


def extract_skills_from_job(job_text):
    """Extract required skills from the job_text using simple keyword matching."""
    skill_keywords = [
        "java", "python", "react", "node", "node.js", "c++",
        "sql", "html", "css", "javascript", "figma", "sketch", "wireframing"
    ]
    text = job_text.lower()
    return [s for s in skill_keywords if s in text]




def show_skill_gap(candidate_skills, jobs):
    st.subheader("🧩 Skill Gap Analysis")
    

    formatted_jobs = []
    for job in jobs:
        formatted_jobs.append({
            "job_id": job["job_id"],
            "job_title": extract_job_title(job["job_text"]),
            "skills_required": extract_skills_from_job(job["job_text"]),
            "similarity_score": job["score"]
        })


    resp = run_skill_gap(candidate_skills, jobs)

    # for item in resp:
    #     st.write(f"### {item['job_title']}")
    #     st.write("Matched:", ", ".join(item["matched_skills"]))
    #     st.write("Missing:", ", ".join(item["missing_skills"]))
    #     st.write(f"Match %: {item['match_percent']}")
    #     st.divider()

    return resp
