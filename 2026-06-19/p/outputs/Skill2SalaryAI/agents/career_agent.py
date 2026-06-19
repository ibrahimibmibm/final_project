ROLE_SKILLS = {
    "Data Analyst": {"SQL", "Python", "Pandas", "Data Visualization", "Statistics", "Power BI"},
    "Data Scientist": {"Python", "SQL", "Machine Learning", "Statistics", "Pandas", "Scikit-Learn", "Data Visualization"},
    "ML Engineer": {"Python", "Machine Learning", "MLOps", "Docker", "Cloud", "Scikit-Learn", "PyTorch"},
    "AI Engineer": {"Python", "NLP", "Generative AI", "MLOps", "Cloud", "FastAPI", "Docker"},
    "Full-Stack Developer": {"JavaScript", "TypeScript", "React", "Python", "SQL", "Docker", "Cloud"},
    "Product Manager": {"Product Strategy", "SQL", "Data Visualization", "A/B Testing", "Leadership"},
}


def career_health(skills: list[str], ats: int, experience: int) -> dict:
    breadth = min(len(skills) * 5, 45)
    exp = min(experience * 4, 25)
    score = round(min(100, breadth + exp + ats * 0.30))
    success = round(min(96, score * 0.72 + min(len(skills), 12) * 1.5), 1)
    return {"health_score": score, "success_probability": success, "signals": ["Resume strength", "Skill breadth", "Experience depth"]}


def skill_gap(target_role: str, skills: list[str]) -> dict:
    required = ROLE_SKILLS.get(target_role, ROLE_SKILLS["AI Engineer"])
    current = set(skills)
    missing = sorted(required - current)
    matched = sorted(required & current)
    readiness = round(len(matched) / max(len(required), 1) * 100)
    return {"target_role": target_role, "matched": matched, "missing": missing, "readiness": readiness}


def career_paths(skills: list[str]) -> list[dict]:
    paths = []
    for role in ROLE_SKILLS:
        gap = skill_gap(role, skills)
        paths.append({"role": role, "fit": gap["readiness"], "next_skills": gap["missing"][:3]})
    return sorted(paths, key=lambda item: item["fit"], reverse=True)


def coach_response(message: str, user: dict, skills: list[str]) -> str:
    target = user.get("target_role") or "AI Engineer"
    gap = skill_gap(target, skills)
    if gap["missing"]:
        focus = ", ".join(gap["missing"][:3])
        return f"For {target}, your strongest move is to build evidence around {focus}. Pair one portfolio project with measurable outcomes and update your resume bullets with metrics."
    return f"You already cover the core {target} skill profile. Shift toward senior signals: architecture decisions, ownership scope, mentoring, and measurable business impact."
