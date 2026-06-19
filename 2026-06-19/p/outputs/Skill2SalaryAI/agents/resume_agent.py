def resume_recommendations(ats_missing: list[str], skills: list[str]) -> list[str]:
    tips = []
    if ats_missing:
        tips.extend(f"Add or strengthen: {item}." for item in ats_missing)
    if len(skills) < 8:
        tips.append("Add a compact skills matrix grouped by language, AI/data, cloud, and tools.")
    tips.append("Rewrite experience bullets with action, technical method, metric, and business result.")
    tips.append("Add links to GitHub, portfolio, LinkedIn, and deployed demos where available.")
    return tips[:6]
