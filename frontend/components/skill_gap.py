import streamlit as st
from api_client import run_skill_gap

def show_skill_gap(candidate_skills, jobs):
    st.subheader("🧩 Skill Gap Analysis")

    # 1️⃣ Candidate skills must be a LIST (backend requirement)
    candidate_skills_list = list(candidate_skills)

    # 2️⃣ Convert jobs → required backend structure
    formatted_jobs = []
    for job in jobs:
        formatted_jobs.append({
            "job_id": job["job_id"],
            "job_title": job.get("job_title", "Unknown"),
            "skills_required": job.get("required_skills", []),
            "similarity_score": job.get("similarity_score", job.get("score", 0))
        })

    # 3️⃣ Call backend with correct payload
    resp = run_skill_gap(candidate_skills_list, formatted_jobs)

    # 4️⃣ Verify backend response
    if not isinstance(resp, list):
        st.error("❌ Backend returned unexpected result. Expected a list.")
        st.json(resp)
        return resp

    # 5️⃣ Render
    for item in resp:
        st.write(f"### {item.get('job_title', 'Unknown')}")
        st.write("Matched:", ", ".join(item.get("matched_skills", [])))
        st.write("Missing:", ", ".join(item.get("missing_skills", [])))
        st.write(f"Match %: {item.get('match_percent', 0)}")
        st.divider()

    return resp
