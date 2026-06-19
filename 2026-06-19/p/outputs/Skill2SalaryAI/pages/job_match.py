import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section
from database.db import fetch_user_skills
from agents.career_agent import career_paths

st.set_page_config(page_title="Job Match | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
section("Job Match Engine", "Rank roles by skill alignment and next-step gaps.")
paths = career_paths(fetch_user_skills(st.session_state["user"]["id"]))
jobs = [{"company": c, "role": p["role"], "match_score": p["fit"], "missing_skills": ", ".join(p["next_skills"])} for c in ["NovaAI", "CloudWorks", "Insight Labs", "DataForge", "ProductOS", "VectorStack"] for p in paths[:1]]
st.dataframe(jobs, use_container_width=True, hide_index=True)
