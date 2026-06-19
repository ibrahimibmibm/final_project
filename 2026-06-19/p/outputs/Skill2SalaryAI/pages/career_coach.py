import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section
from database.db import fetch_user_skills
from agents.career_agent import coach_response

st.set_page_config(page_title="Career Coach | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
section("AI Career Coach", "Ask for resume, salary, interview, learning, and job-search guidance.")
if "chat" not in st.session_state:
    st.session_state.chat = []
for item in st.session_state.chat:
    st.chat_message(item["role"]).write(item["content"])
message = st.chat_input("Ask your career coach")
if message:
    st.session_state.chat.append({"role": "user", "content": message})
    response = coach_response(message, user, fetch_user_skills(user["id"]))
    st.session_state.chat.append({"role": "assistant", "content": response})
    st.rerun()
