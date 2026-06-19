import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section, tag_cloud
from components.charts import gauge
from database.db import fetch_user_skills
from agents.career_agent import skill_gap

st.set_page_config(page_title="Skill Gap | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
skills = fetch_user_skills(user["id"])
target = st.selectbox("Target role", ["AI Engineer", "ML Engineer", "Data Scientist", "Data Analyst", "Full-Stack Developer", "Product Manager"], index=0)
gap = skill_gap(target, skills)
section("Skill Gap Analysis", "Compare your current skill set with role expectations.")
st.plotly_chart(gauge(gap["readiness"], "Role Readiness"), use_container_width=True)
st.subheader("Matched skills"); tag_cloud(gap["matched"] or ["No matches yet"])
st.subheader("Missing skills"); tag_cloud(gap["missing"] or ["Core role skills covered"])
