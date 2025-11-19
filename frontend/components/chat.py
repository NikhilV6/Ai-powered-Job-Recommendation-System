import streamlit as st
from api_client import chat_to_bot

def chatbot_section(candidate_skills=None, skill_gap_jobs=None):
    st.subheader("💬 Career Assistant Chatbot")

    if "session_id" not in st.session_state:
        st.session_state.session_id = ""

    msg = st.chat_input("Ask something about your career, jobs, skills...")

    if msg:
        st.chat_message("user").write(msg)

        resp = chat_to_bot(
            st.session_state.session_id,
            msg,
            generate_plan=False
        )

        st.session_state.session_id = resp["session_id"]

        answer = resp["answer"]["answer_summary"]
        st.chat_message("assistant").markdown(answer)
