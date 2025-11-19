import streamlit as st
from api_client import get_recommended_jobs

def show_job_recommendations(skills):
    st.subheader("🎯 Recommended Jobs")

    # Call backend
    if isinstance(skills, (list, tuple)):
        skills = ",".join(str(s).strip() for s in skills)
    resp = get_recommended_jobs(skills)

    # Debug: show raw JSON
    st.json(resp)
    
    
    # Correct key from backend
    jobs = resp["recommendations"]

    # Render each job card
    for job in jobs:
        st.write(f"**Job ID:** {job['job_id']}")
        st.write(f"**Description:** {job['job_text']}")
        st.write(f"**Score:** `{job['score']:.2f}`")
        st.divider()

    return jobs
