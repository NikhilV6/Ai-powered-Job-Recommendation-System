import os
import pandas as pd
from app.services.vector_index import build_index_fast
import time

def normalize_skills(raw):
    if pd.isna(raw):
        return ""
    # split by space OR comma → normalize
    parts = raw.replace(",", " ").split()
    return ", ".join([p.strip().lower() for p in parts])

def main():
    start_time = time.time()
    
    print("Loading cleaned dataset...")

    PROJECT_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../")
    )

    DATA_PATH = os.path.join(PROJECT_ROOT, "data", "job_dataset.csv")

    print("Dataset path:", DATA_PATH)

    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded with {len(df)} rows.")

    # Normalize skills
    print("Normalizing skills...")
    df["skills_norm"] = df["skills"].apply(normalize_skills)

    # Create enhanced embedding text
    print("Creating job text descriptions...")
    df["job_text"] = (
        "Job Title: " + df["Job Title"].fillna("") + "\n" +
        "Role: " + df["Role"].fillna("") + "\n" +
        "Description: " + df["Job Description"].fillna("") + "\n" +
        "Required Skills: " + df["skills_norm"].fillna("") + "\n" +
        "Company: " + df["Company"].fillna("") + "\n" +
        "Experience: " +
            df["experience_min"].astype(str).fillna("0") + " to " +
            df["experience_max"].astype(str).fillna("0") + " years\n" +
        "Qualification: " + df["qualification_level"].fillna("")
    )

    print("Preparing records...")
    records = []

    for _, row in df.iterrows():
        records.append({
            "job_text": row["job_text"],
            "skills": row["skills_norm"].split(", ") if isinstance(row["skills_norm"], str) and row["skills_norm"] else [],
            # Add all metadata fields
            "job_title": row["Job Title"] if pd.notna(row["Job Title"]) else "",
            "role": row["Role"] if pd.notna(row["Role"]) else "",
            "description": row["Job Description"] if pd.notna(row["Job Description"]) else "",
            "company": row["Company"] if pd.notna(row["Company"]) else "",
            "location": row["location"] if pd.notna(row["location"]) else "",
            "experience_min": int(row["experience_min"]) if pd.notna(row["experience_min"]) else 0,
            "experience_max": int(row["experience_max"]) if pd.notna(row["experience_max"]) else 0,
            "qualification_level": row["qualification_level"] if pd.notna(row["qualification_level"]) else "",
            "salary_min": int(row["salary_min"]) if pd.notna(row["salary_min"]) else 0,
            "salary_max": int(row["salary_max"]) if pd.notna(row["salary_max"]) else 0,
            "posting_date": row["Job Posting Date"] if pd.notna(row["Job Posting Date"]) else ""
        })

    print(f"Building FAISS index with batch processing...")
    build_index_fast(records)

    elapsed = time.time() - start_time
    print(f"\n🎉 FAISS index created successfully in {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)!")

if __name__ == "__main__":
    main()