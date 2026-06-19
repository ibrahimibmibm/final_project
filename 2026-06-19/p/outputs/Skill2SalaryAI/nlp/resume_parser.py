from pathlib import Path

import pdfplumber
from PyPDF2 import PdfReader


def parse_resume(uploaded_file) -> str:
    suffix = Path(uploaded_file.name).suffix.lower()
    if suffix == ".pdf":
        return parse_pdf(uploaded_file)
    data = uploaded_file.getvalue()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="ignore")


def parse_pdf(uploaded_file) -> str:
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        uploaded_file.seek(0)
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    return text.strip()


def ats_score(text: str, skills: list[str]) -> tuple[int, list[str]]:
    checks = {
        "Contact details": any(token in text.lower() for token in ["email", "@", "phone", "linkedin"]),
        "Measurable impact": any(char.isdigit() for char in text),
        "Skills section": "skill" in text.lower() or len(skills) >= 5,
        "Experience section": any(word in text.lower() for word in ["experience", "work", "employment"]),
        "Project evidence": "project" in text.lower() or "github" in text.lower(),
        "Education section": "education" in text.lower() or "degree" in text.lower(),
    }
    score = round(sum(checks.values()) / len(checks) * 100)
    missing = [name for name, ok in checks.items() if not ok]
    return score, missing
