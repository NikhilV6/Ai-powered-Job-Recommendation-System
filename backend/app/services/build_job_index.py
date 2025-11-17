import os
import pandas as pd
from app.services.vector_index import build_index

def main():
    print("Loading cleaned dataset...")

    PROJECT_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../")
    )

    DATA_PATH = os.path.join(PROJECT_ROOT, "data", "job_dataset.csv")

    print("Dataset path:", DATA_PATH)

    df = pd.read_csv(DATA_PATH)
    print("Dataset loaded with", len(df), "rows.")

    # Build combined job text
    df["job_text"] = (
        df["Job Title"].fillna("") + " " +
        df["Role"].fillna("") + " " +
        df["Job Description"].fillna("") + " " +
        df["skills"].fillna("")
    )

    texts = df["job_text"].astype(str).tolist()

    print("Building FAISS index...")
    build_index(texts)

    print("🎉 FAISS index created successfully!")

if __name__ == "__main__":
    main()
