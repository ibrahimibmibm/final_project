import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import metric_card, section, tag_cloud
from components.charts import gauge
from database.db import fetch_user_skills, latest_resume
from agents.career_agent import career_health, career_paths

st.set_page_config(page_title="Dashboard | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
skills = fetch_user_skills(user["id"])
resume = latest_resume(user["id"]) or {"ats_score": 0}
health = career_health(skills, int(resume.get("ats_score") or 0), int(user.get("experience") or 0))

section("Dashboard", "Live career intelligence from your profile, resume, and skills.")
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Skills", str(len(skills)), "Extracted from resume")
with c2:
    metric_card("ATS Score", f"{int(resume.get('ats_score') or 0)}%", "Resume readiness")
with c3:
    metric_card("Career Health", f"{health['health_score']}%", "Overall profile strength")
with c4:
    metric_card("Success Probability", f"{health['success_probability']}%", "Near-term role readiness")

left, right = st.columns([1, 1])
with left:
    st.plotly_chart(gauge(health["health_score"], "Career Health"), use_container_width=True)
with right:
    st.plotly_chart(gauge(health["success_probability"], "Success Probability"), use_container_width=True)
section("Skill Signal")
tag_cloud(skills or ["Upload a resume to extract skills"])
section("Best-Fit Career Paths")
st.dataframe(career_paths(skills), use_container_width=True, hide_index=True)
