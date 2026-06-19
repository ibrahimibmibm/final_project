from pathlib import Path

import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section
from database.db import fetch_user_skills, latest_resume
from agents.career_agent import career_health, career_paths, skill_gap

st.set_page_config(page_title="Career Report | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
skills = fetch_user_skills(user["id"])
resume = latest_resume(user["id"]) or {"ats_score": 0}
health = career_health(skills, int(resume.get("ats_score") or 0), int(user.get("experience") or 0))
target = user.get("target_role") or "AI Engineer"
gap = skill_gap(target, skills)

def build_pdf() -> Path:
    report_dir = Path("reports"); report_dir.mkdir(exist_ok=True)
    path = report_dir / f"career_report_user_{user['id']}.pdf"
    c = canvas.Canvas(str(path), pagesize=letter)
    y = 740
    for line in [
        "Skill2Salary AI Career Report",
        f"Name: {user['name']}",
        f"Target role: {target}",
        f"ATS score: {resume.get('ats_score') or 0}%",
        f"Career health: {health['health_score']}%",
        f"Success probability: {health['success_probability']}%",
        f"Skills: {', '.join(skills) or 'No skills extracted yet'}",
        f"Missing skills: {', '.join(gap['missing']) or 'Core role skills covered'}",
    ]:
        c.drawString(50, y, line[:105]); y -= 28
    c.save()
    return path

section("Downloadable AI Career Report PDF", "Generate a concise report from your latest career intelligence.")
st.write("Career paths")
st.dataframe(career_paths(skills), use_container_width=True, hide_index=True)
if st.button("Generate PDF", use_container_width=True):
    pdf = build_pdf()
    st.success(f"Report generated: {pdf}")
    st.download_button("Download report", pdf.read_bytes(), file_name=pdf.name, mime="application/pdf", use_container_width=True)
