
# ------------------------------------------------------------------------------
# backend/app/services/resume_parser.py
# Robust resume parser: PDF extraction, basic DOCX support, skill extraction using a skills list,
# regex-based contact info and experience extraction, and lightweight normalization.

import re
import json
from pathlib import Path
from typing import Dict, List, Optional

import pdfplumber
import docx2txt
import spacy
from rapidfuzz import process, fuzz

from app.core.config import settings

# load spaCy model lazily
_nlp = None

def _get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except Exception:
            # if not available, fall back to blank English
            _nlp = spacy.blank("en")
    return _nlp

# load skills master list (lowercase normalized set)
_skills_master = None

def _load_skills_master():
    global _skills_master
    if _skills_master is None:
        path = Path(settings.DATA_DIR) / settings.SKILLS_FILE
        if not path.exists():
            # fallback small list
            _skills_master = set(["python","java","c++","sql","django","flask","react","node.js","docker","kubernetes","aws","git","nlp","tensorflow","pytorch"]) 
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # data can be list or dict
            if isinstance(data, dict):
                skills = list(data.keys())
            else:
                skills = data
            _skills_master = set(s.strip().lower() for s in skills if s)
    return _skills_master

# --- TEXT EXTRACTION HELPERS ---

def extract_text_from_pdf(path: str) -> str:
    """Extract text from PDF using pdfplumber. Returns raw text."""
    text_chunks = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
    except Exception:
        pass
    return "\n".join(text_chunks)


def extract_text_from_docx(path: str) -> str:
    try:
        return docx2txt.process(path) or ""
    except Exception:
        return ""


def extract_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        text = extract_text_from_pdf(path)
    elif suffix in [".docx", ".doc"]:
        text = extract_text_from_docx(path)
    else:
        text = p.read_text(encoding="utf-8", errors="ignore")
    return text

# --- INFORMATION EXTRACTION ---

PHONE_RE = re.compile(r"(\+?\d[\d\-\s()]{7,}\d)")
EMAIL_RE = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
YEARS_EXP_RE = re.compile(r"(\d+)\+?\s*(?:years|yrs|year)")


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    phones = PHONE_RE.findall(text)
    emails = EMAIL_RE.findall(text)
    phone = phones[0] if phones else None
    email = emails[0] if emails else None
    return {"phone": phone, "email": email}


def extract_experience_years(text: str) -> Optional[int]:
    # heuristic: find explicit "X years" or derive from dates
    m = YEARS_EXP_RE.search(text.lower())
    if m:
        try:
            return int(m.group(1))
        except Exception:
            pass
    # fallback: find ranges like 2018 - 2021 and compute unique years
    years = re.findall(r"(20\d{2}|19\d{2})", text)
    if years:
        yrs = sorted(set(int(y) for y in years))
        if len(yrs) >= 2:
            # crude approximation: span of years
            return yrs[-1] - yrs[0]
    return None


def extract_name(text: str) -> Optional[str]:
    # use spaCy NER to find PERSON in top lines
    nlp = _get_nlp()
    doc = nlp(text[:2000])
    # prefer entity labeled PERSON in first 120 chars
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text.strip()
    # fallback: first line that looks like a name (letters and spaces, <=4 tokens)
    first_lines = [l.strip() for l in text.splitlines() if l.strip()]
    if first_lines:
        candidate = first_lines[0]
        if len(candidate.split()) <= 4 and re.match(r"^[A-Za-z .'-]+$", candidate):
            return candidate
    return None

# Skill extraction uses fuzzy matching to match tokens / noun chunks to a skills master list

def extract_skills(text: str, top_k: int = 60, scorer=fuzz.token_sort_ratio) -> List[str]:
    skills_master = _load_skills_master()
    text_low = text.lower()

    # quick exact matches
    found = set([s for s in skills_master if s in text_low])

    # use spaCy to extract candidate phrases
    nlp = _get_nlp()
    doc = nlp(text[:100000])  # cap length for performance
    candidates = set()
    # nouns & noun_chunks
    for chunk in doc.noun_chunks:
        c = chunk.text.strip().lower()
        if 2 <= len(c) <= 50:
            candidates.add(c)
    for ent in doc.ents:
        candidates.add(ent.text.strip().lower())

    # also split text into potential tokens
    tokens = re.findall(r"[a-zA-Z#+.\-]{2,}", text_low)
    for t in tokens:
        if len(t) <= 40:
            candidates.add(t)

    # fuzzy match candidates to skills master
    # rapidfuzz.process.extract returns list of tuples (match, score, idx)
    choices = list(skills_master)
    for cand in candidates:
        match = process.extractOne(cand, choices, scorer=scorer)
        if match and match[1] >= 80:  # threshold; tweak as needed
            found.add(match[0])

    # return sorted list by occurrence in text
    found_list = sorted(found, key=lambda s: text_low.find(s))
    return found_list

# Project / education extraction (lightweight heuristics)

def extract_education(text: str) -> List[str]:
    degrees = ["bachelor", "b.sc", "b.e", "b.tech", "master", "m.sc", "m.tech", "m.e", "mca", "phd", "ph.d"]
    found = []
    low = text.lower()
    for d in degrees:
        if d in low:
            found.append(d)
    return found

# main parse function

def parse_resume(path: str) -> Dict:
    """Return a normalized profile dict from resume file path."""
    text = extract_text(path)
    profile = {}
    profile["raw_text"] = text
    profile["name"] = extract_name(text)
    profile.update(extract_contact_info(text))
    profile["experience_years"] = extract_experience_years(text)
    profile["skills"] = extract_skills(text)
    profile["education"] = extract_education(text)
    return profile

