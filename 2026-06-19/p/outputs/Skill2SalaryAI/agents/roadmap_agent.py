def learning_roadmap(missing_skills: list[str], target_role: str) -> dict:
    skills = missing_skills or ["Portfolio storytelling", "System design", "Interview practice"]
    weekly = []
    for idx, skill in enumerate(skills[:6], start=1):
        weekly.append({"week": idx, "focus": skill, "deliverable": f"Complete a focused {skill} mini-project or case study."})
    monthly = [
        {"month": 1, "theme": "Foundation", "goal": f"Close the top gaps for {target_role}."},
        {"month": 2, "theme": "Portfolio", "goal": "Publish one project with metrics, architecture notes, and a short demo."},
        {"month": 3, "theme": "Market readiness", "goal": "Run mock interviews, tune resume keywords, and apply to matched roles."},
    ]
    projects = [
        f"{target_role} capstone with dashboard and written business impact",
        "End-to-end data product with ingestion, model, UI, and deployment notes",
        "Portfolio case study converting a messy problem into a measurable outcome",
    ]
    certifications = ["AWS Cloud Practitioner", "Google Data Analytics", "Microsoft Azure AI Fundamentals", "DeepLearning.AI Machine Learning"]
    return {"weekly": weekly, "monthly": monthly, "projects": projects, "certifications": certifications}
