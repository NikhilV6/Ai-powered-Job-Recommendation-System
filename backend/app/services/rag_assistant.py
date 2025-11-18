from typing import Dict, Any, List, Optional
import uuid
import json
import ast

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.services.chat_memory import chat_memory
from app.services.rag_retriever import build_context_string
from app.services.learning_path_service import generate_learning_path


def get_llm():
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set in .env or environment.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.4,
    )
    return llm


def format_history_text(history) -> str:
    if not history:
        return "No previous conversation. This is the first user question."

    lines = []
    for msg in history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            lines.append(f"User: {content}")
        else:
            lines.append(f"Assistant: {content}")
    return "\n".join(lines)


def _default_answer_json(summary: str = "No answer available.") -> Dict[str, Any]:
    return {
        "answer_summary": summary,
        "career_options": [],
        "guidance": [],
    }


def _parse_llm_json_output(text: str) -> Dict[str, Any]:
    """
    Try to parse the LLM output as JSON.
    If it fails, return a minimal default structure.
    """
    if not text:
        return _default_answer_json()

    try:
        data = json.loads(text)
    except Exception:
        try:
            # Gemini sometimes returns Python-like repr, try literal_eval
            data = ast.literal_eval(text)
        except Exception:
            return _default_answer_json(summary="Failed to parse JSON from model output.")

    if not isinstance(data, dict):
        return _default_answer_json(summary="Model output was not a JSON object.")

    # minimal safety: ensure keys exist
    if "answer_summary" not in data:
        data["answer_summary"] = "No summary provided."
    if "career_options" not in data:
        data["career_options"] = []
    if "guidance" not in data:
        data["guidance"] = []

    return data


def chat_career_assistant(
    message: str,
    session_id: Optional[str],
    top_k: int = 5,
    generate_learning_path_flag: bool = False,
    candidate_skills: Optional[List[str]] = None,
    target_skills: Optional[List[str]] = None,
    job_title: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Main RAG + Mongo memory + strict-JSON answer + optional learning path.
    """

    # 1. Ensure session_id (default for docs testing)
    if not session_id or session_id.strip() == "":
        session_id = "docs-demo-session"

    # 2. Load history from Mongo
    history = chat_memory.get_history(session_id)
    history_text = format_history_text(history)

    # 3. RAG context from FAISS
    context_text = build_context_string(message, top_k=top_k)

    # 4. System instructions: STRICT JSON
    system_instructions = """
You are an AI-powered career assistant for software and technology jobs.

You MUST ALWAYS respond with a STRICT JSON object, with this EXACT schema:

{
  "answer_summary": "short 1-2 sentence summary of your answer",
  "career_options": [
    {
      "role": "string, name of the role (e.g., 'Data Analyst')",
      "core_skills": ["list", "of", "key", "skills"],
      "why_suitable": "1-3 short sentences explaining why this role fits the user",
      "next_steps": ["step 1", "step 2", "step 3"]
    }
  ],
  "guidance": [
    "short actionable tip 1",
    "short actionable tip 2"
  ]
}

RULES:
- DO NOT include any text before or after the JSON.
- DO NOT use markdown.
- DO NOT wrap JSON in backticks.
- Keep texts short and crisp.
- If the context is not useful, you can ignore it but still fill the JSON structure.
"""

    full_prompt = f"""
{system_instructions}

Conversation History:
{history_text}

Retrieved Context (from internal job dataset via FAISS):
{context_text}

User Question:
{message}

Return ONLY a JSON object that follows the schema above. No extra text.
"""

    # 5. Call LLM
    llm = get_llm()
    response = llm.invoke(full_prompt)
    raw_text = response.content

    # 6. Parse JSON
    answer_json = _parse_llm_json_output(raw_text)

    # 7. Persist messages in Mongo memory (raw text stored for traceability)
    chat_memory.add_message(session_id, "user", message)
    chat_memory.add_message(session_id, "assistant", raw_text)

    # 8. Optional learning path generation
    learning_plan = None
    if generate_learning_path_flag and candidate_skills and target_skills:
        learning_plan = generate_learning_path(
            candidate_skills=candidate_skills,
            target_skills=target_skills,
            use_llm=True,
            job_title=job_title,
        )

    return {
        "session_id": session_id,
        "answer_json": answer_json,
        "used_top_k": top_k,
        "learning_path": learning_plan,
    }
