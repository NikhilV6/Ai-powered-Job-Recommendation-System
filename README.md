# AI-Powered Job Recommendation System

A full‑stack **AI-driven career assistant** designed to:

* Parse resumes
* Recommend jobs using FAISS vector search
* Analyze skill gaps
* Generate personalized learning paths
* Provide a conversational RAG chatbot with memory
* Used **Langchain** for all LLM tasks
* Persist chat memory in MongoDB

This README covers:

* System architecture
* Directory structure
* Environment setup
* How to run the backend
* API modules overview
* Future enhancements

---

# 🚀 Features Implemented

## ✅ **1. Resume Parser**

* Extracts:

  * Skills
  * Education
  * Experience
  * Projects
* Uses NLP + custom dictionaries.

## ✅ **2. Job Dataset Preprocessing**

* Cleans 10L+ job entries
* Builds `job_text` for embeddings
* Extracts `skills_required`

## ✅ **3. Embeddings + FAISS Vector Index**

* Sentence-Transformers MiniLM embeddings
* FAISS index for similarity search
* Top‑K job retrieval via vector search

## ✅ **4. Job Recommendation System**

* Candidate vector vs FAISS search
* Returns ranked jobs with similarity score

## ✅ **5. Skill Gap Analyzer**

* Compares:

  * candidate_skills
  * job.required_skills
* Computes:

  * matched skills
  * missing skills
  * match percentage

## ✅ **6. Learning Path Generator**

* Rule‑based weekly plan
* LLM‑enhanced detailed syllabus
* Produces structured JSON output

## ✅ **7. RAG Conversational Career Assistant**

* FAISS-based context retrieval
* Gemini 2.5 Flash responses
* Strict JSON output every time

## ✅ **8. Persistent Memory (MongoDB)**

* Stores chat turns per `session_id`
* Retrieval on next message

---

# 📁 Directory Structure

```
backend/
│   .env
│   requirements.txt
│   README.md
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │     ├── config.py
│   │     ├── database.py
│   │
│   ├── services/
│   │     ├── resume_parser.py
│   │     ├── preprocessing.py
│   │     ├── vector_index.py
│   │     ├── skill_gap.py
│   │     ├── learning_path_rules.py
│   │     ├── learning_path_llm.py
│   │     ├── learning_path_service.py
│   │     ├── rag_retriever.py
│   │     ├── chat_memory.py
│   │     ├── rag_assistant.py
│   │
│   ├── api/
│   │   ├── v1/
│   │   │     ├── resume.py
│   │   │     ├── recommend.py
│   │   │     ├── skill_gap.py
│   │   │     ├── learning_path.py
│   │   │     ├── chat_assistant.py
│   │
└── data/
       ├── cleaned_jobs.csv
       ├── skills_master.json
```

---

# 🛠️ Environment Setup (Conda Virtual Environment)

### 1️⃣ Install Conda (if not installed)

[https://www.anaconda.com/download](https://www.anaconda.com/download)

### 2️⃣ Create project environment

```bash
conda create -n ai-job python=3.10 -y
```

### 3️⃣ Activate environment

```bash
conda activate ai-job
```

### 4️⃣ Install dependencies

From inside the `backend/` folder:

```bash
pip install -r requirements.txt
```

If FAISS CPU errors occur on Windows:

```bash
pip install faiss-cpu
```

### 5️⃣ Install MongoDB locally

* Download from: [https://www.mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
* Run Mongo using default URI:

```
mongodb://localhost:27017
```

### 6️⃣ Create `.env` file in `backend/`

```env
GEMINI_API_KEY=your_gemini_2_5_flash_key_here
MONGO_URI=mongodb://localhost:27017
```

---

# ▶️ How to Run the Backend

### 1️⃣ Navigate to backend

```bash
cd backend
```

### 2️⃣ Activate environment

```bash
conda activate ai-job
```

### 3️⃣ Start server

```bash
uvicorn app.main:app --reload --port 8000
```

### 4️⃣ Open API docs

Visit:

```
http://localhost:8000/docs
```

You can now:

* Upload resumes
* Test job recommendation
* Test learning path
* Use the chatbot with memory

---

# 🧠 API Overview

### **/resume/upload**

Parse resume → extract skills, education, etc.

### **/recommend**

Vector search → Top‑K similar jobs.

### **/skill-gap-simple/**

Input: candidate skills + job skills → compute gaps.

### **/learning-path/**

Generate:

* weekly curriculum
* optional LLM-enhanced path

### **/chat/** (RAG + Memory)

Input:

* `message`
* `session_id` (optional)
* skill lists (optional)

Output (strict JSON):

```json
{
  "answer_summary": "...",
  "career_options": [ ... ],
  "guidance": [ ... ]
}
```

---

# 💡 Future Improvements

* Add authentication & user accounts
* Deploy FAISS on serverless endpoint
* Add dashboard for analytics
* Add support for ATS resume scoring
* Containerization with Docker

---

# 🙌 Credits

Developed as a Final Year B.Tech Information Technology Project.

Includes:

* FastAPI backend
* FAISS vector search
* Langchain with Gemini 2.5 Flash LLM integration
* MongoDB memory persistence
* Full modular ML/NLP pipeline

---

# 📞 Need Help?

Ask anytime — the assistant is here to help you guide in your career! 💙

