import streamlit as st
from components.theme import load_css
from database.db import create_user, authenticate, init_db

st.set_page_config(page_title="Sign Up | Skill2Salary AI", layout="wide")
init_db(); load_css()
st.markdown("<div class='hero'><h1>Create Your Profile</h1><p>Start converting your skills into salary strategy.</p></div>", unsafe_allow_html=True)
name = st.text_input("Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
title = st.text_input("Current title")
target_role = st.selectbox("Target role", ["AI Engineer", "ML Engineer", "Data Scientist", "Data Analyst", "Full-Stack Developer", "Product Manager"])
experience = st.number_input("Years of experience", 0, 40, 2)
location = st.text_input("Location", "Remote")
if st.button("Create account", use_container_width=True):
    if not name or not email or len(password) < 6:
        st.error("Enter a name, valid email, and password with at least 6 characters.")
    elif create_user(name, email, password, title, target_role, experience, location):
        st.session_state["user"] = authenticate(email, password)
        st.success("Account created.")
        st.switch_page("app.py")
    else:
        st.error("That email is already registered.")
