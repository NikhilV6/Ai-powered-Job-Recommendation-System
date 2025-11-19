import streamlit as st

from components.resume_upload import resume_upload_section
from components.job_results import show_job_recommendations
from components.skill_gap import show_skill_gap
from components.chat import chatbot_section


st.set_page_config(page_title="AI Career Assistant", layout="wide")

st.title("🤖 AI-Powered Career Assistant")


candidate_skills = resume_upload_section()

if candidate_skills:
    jobs = show_job_recommendations(candidate_skills)
    skill_gap_jobs = show_skill_gap(candidate_skills, jobs)
    chatbot_section(candidate_skills, skill_gap_jobs)
else:
    st.info("Upload a resume to begin.")
