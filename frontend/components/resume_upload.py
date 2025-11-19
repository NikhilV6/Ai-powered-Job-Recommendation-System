import streamlit as st
from api_client import upload_resume

def resume_upload_section():
    st.subheader("📤 Upload Resume")

    uploaded = st.file_uploader("Upload PDF Resume", type=["pdf"])

    if uploaded:
        with st.spinner("Extracting skills..."):
            resp = upload_resume(uploaded.read())
            st.success("Resume processed!")
            return resp["profile"]["skills"]


    return None
