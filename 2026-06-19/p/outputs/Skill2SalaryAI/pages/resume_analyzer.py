from pathlib import Path

import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section, tag_cloud
from components.charts import gauge
from database.db import save_resume, save_skills
from nlp.resume_parser import parse_resume, ats_score
from nlp.skill_extractor import extract_skills, skill_categories
from agents.resume_agent import resume_recommendations

st.set_page_config(page_title="Resume Analyzer | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
section("Resume Analyzer", "Upload a PDF or text resume to extract skills and ATS signals.")
uploaded = st.file_uploader("Resume file", type=["pdf", "txt"])
if uploaded:
    text = parse_resume(uploaded)
    skills = extract_skills(text)
    score, missing = ats_score(text, skills)
    save_resume(user["id"], uploaded.name, text, score)
    save_skills(user["id"], skills)
    upload_path = Path("uploads") / uploaded.name
    upload_path.write_bytes(uploaded.getvalue())
    c1, c2 = st.columns([1, 2])
    with c1:
        st.plotly_chart(gauge(score, "ATS Score"), use_container_width=True)
    with c2:
        tag_cloud(skills)
        st.json(skill_categories(skills))
    section("Recommendations")
    for tip in resume_recommendations(missing, skills):
        st.write(f"- {tip}")
    with st.expander("Extracted resume text"):
        st.write(text[:8000])
