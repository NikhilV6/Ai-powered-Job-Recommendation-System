import streamlit as st
from api_client import get_recommended_jobs

def show_job_recommendations(skills):
    st.subheader("🎯 Recommended Jobs")

    # Convert list → string for API
    if isinstance(skills, (list, tuple)):
        skills = ",".join(str(s).strip() for s in skills)
    
    # Call backend
    resp = get_recommended_jobs(skills)

    # Debug (optional)
    # st.json(resp)

    # New response structure
    jobs = resp.get("recommendations", [])

    # Render each job card
    for job in jobs:
        st.markdown(f"### 🧑‍💻 {job['job_title']} — *{job['role']}*")
        
        st.write(f"**Company:** {job['company']}")
        st.write(f"**Location:** {job['location']}")
        
        exp = job.get("experience_range", {})
        st.write(f"**Experience:** {exp.get('min', '?')} - {exp.get('max', '?')} years")

        st.write(f"**Qualification:** {job['qualification_level'].title()}")

        salary = job.get("salary_range", {})
        st.write(f"**Salary:** ${salary.get('min', '?'):,} - ${salary.get('max', '?'):,}")

        st.write(f"**Posted On:** {job['posting_date']}")
        
        st.write(f"**Required Skills:** {', '.join(job['required_skills'])}")

        st.write(f"**Similarity Score:** `{job['similarity_score']:.3f}`")

        st.write("**Description:**")
        st.write(job["description"])

        st.divider()

    return jobs
