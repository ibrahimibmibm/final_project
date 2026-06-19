import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section
from database.db import fetch_user_skills
from agents.career_agent import skill_gap
from agents.roadmap_agent import learning_roadmap

st.set_page_config(page_title="Roadmap | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
target = user.get("target_role") or "AI Engineer"
gap = skill_gap(target, fetch_user_skills(user["id"]))
plan = learning_roadmap(gap["missing"], target)
section("Personalized Learning Roadmap", f"Target role: {target}")
st.subheader("Weekly Plan"); st.dataframe(plan["weekly"], use_container_width=True, hide_index=True)
st.subheader("Monthly Plan"); st.dataframe(plan["monthly"], use_container_width=True, hide_index=True)
st.subheader("Project Recommendations"); [st.write(f"- {p}") for p in plan["projects"]]
st.subheader("Certification Recommendations"); [st.write(f"- {c}") for c in plan["certifications"]]
