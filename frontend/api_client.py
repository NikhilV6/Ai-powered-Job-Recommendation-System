import requests

BASE_URL = "http://127.0.0.1:8000"   # FastAPI backend

def upload_resume(file_bytes):
    files = {"file": ("resume.pdf", file_bytes, "application/pdf")}
    r = requests.post(f"{BASE_URL}/resume/upload", files=files)
    return r.json()

def get_recommended_jobs(skills):
    r = requests.post(f"{BASE_URL}/recommend", json={"text": skills})
    return r.json()

def run_skill_gap(candidate_skills, jobs):
    body = {"candidate": {"candidate_skills": candidate_skills}, "jobs": jobs}
    r = requests.post(f"{BASE_URL}/skill-gap-simple/", json=body)
    return r.json()

def chat_to_bot(session_id, message, generate_plan=False, candidate=None, target=None, job_title=None):
    payload = {
        "message": message,
        "session_id": session_id,
        "generate_learning_path": generate_plan,
        "candidate_skills": candidate,
        "target_skills": target,
        "job_title": job_title
    }
    r = requests.post(f"{BASE_URL}/chat", json=payload)
    return r.json()
