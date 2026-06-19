import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section
from components.charts import gauge
from database.db import fetch_user_skills, latest_resume, save_json
from agents.career_agent import career_health

st.set_page_config(page_title="Career Score | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
skills = fetch_user_skills(user["id"])
resume = latest_resume(user["id"]) or {"ats_score": 0}
score = career_health(skills, int(resume.get("ats_score") or 0), int(user.get("experience") or 0))
save_json("career_scores", user["id"], score)
section("Career Score", "Career health and success probability combine resume quality, skills, and experience.")
c1, c2 = st.columns(2)
c1.plotly_chart(gauge(score["health_score"], "Career Health"), use_container_width=True)
c2.plotly_chart(gauge(score["success_probability"], "Success Probability"), use_container_width=True)
st.write("Signals reviewed:", ", ".join(score["signals"]))
