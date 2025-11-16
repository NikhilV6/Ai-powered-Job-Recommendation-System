import pytest
from app.services.resume_parser import parse_resume


def test_parse_sample_txt(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text(
        "John Doe\n"
        "Email: john.doe@example.com\n"
        "Experience: 3 years\n"
        "Skills: Python, SQL, Docker"
    )

    out = parse_resume(str(sample))

    assert out["name"] is not None
    assert "python" in [s.lower() for s in out["skills"]]
    assert out["experience_years"] == 3
