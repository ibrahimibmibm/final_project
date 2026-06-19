import re

SKILL_CATALOG = {
    "Python": ["python"], "JavaScript": ["javascript", "js"], "TypeScript": ["typescript", "ts"],
    "SQL": ["sql", "postgres", "mysql", "sqlite"], "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "neural"], "NLP": ["nlp", "natural language"],
    "Generative AI": ["generative ai", "llm", "large language model", "prompt engineering"],
    "Pandas": ["pandas"], "NumPy": ["numpy"], "Scikit-Learn": ["scikit", "sklearn"],
    "TensorFlow": ["tensorflow"], "PyTorch": ["pytorch"], "React": ["react"],
    "Streamlit": ["streamlit"], "FastAPI": ["fastapi"], "Django": ["django"],
    "Flask": ["flask"], "Docker": ["docker"], "Kubernetes": ["kubernetes", "k8s"],
    "AWS": ["aws", "amazon web services"], "Azure": ["azure"], "GCP": ["gcp", "google cloud"],
    "MLOps": ["mlops", "model deployment"], "Git": ["git", "github"], "Tableau": ["tableau"],
    "Power BI": ["power bi"], "Data Visualization": ["visualization", "plotly", "matplotlib", "seaborn"],
    "Statistics": ["statistics", "statistical"], "A/B Testing": ["a/b", "ab testing"],
    "Leadership": ["leadership", "mentoring"], "Product Strategy": ["product strategy", "roadmap"],
}


def extract_skills(text: str) -> list[str]:
    normalized = re.sub(r"[^a-zA-Z0-9+#./ ]+", " ", text.lower())
    found = []
    for skill, aliases in SKILL_CATALOG.items():
        if any(re.search(rf"\b{re.escape(alias)}\b", normalized) for alias in aliases):
            found.append(skill)
    return sorted(set(found))


def skill_categories(skills: list[str]) -> dict[str, list[str]]:
    ai = {"Machine Learning", "Deep Learning", "NLP", "Generative AI", "MLOps", "Scikit-Learn", "TensorFlow", "PyTorch"}
    cloud = {"AWS", "Azure", "GCP", "Docker", "Kubernetes"}
    frontend = {"React", "JavaScript", "TypeScript"}
    data = {"SQL", "Pandas", "NumPy", "Data Visualization", "Statistics", "Tableau", "Power BI", "A/B Testing"}
    groups = {"AI/ML": [], "Cloud/DevOps": [], "Frontend": [], "Data": [], "General": []}
    for skill in skills:
        if skill in ai:
            groups["AI/ML"].append(skill)
        elif skill in cloud:
            groups["Cloud/DevOps"].append(skill)
        elif skill in frontend:
            groups["Frontend"].append(skill)
        elif skill in data:
            groups["Data"].append(skill)
        else:
            groups["General"].append(skill)
    return {k: v for k, v in groups.items() if v}
