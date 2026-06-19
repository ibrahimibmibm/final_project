import streamlit as st
from components.theme import load_css
from database.db import authenticate, init_db

st.set_page_config(page_title="Login | Skill2Salary AI", layout="wide")
init_db(); load_css()
st.markdown("<div class='hero'><h1>Welcome Back</h1><p>Your career intelligence workspace is ready.</p></div>", unsafe_allow_html=True)
email = st.text_input("Email")
password = st.text_input("Password", type="password")
if st.button("Login", use_container_width=True):
    user = authenticate(email, password)
    if user:
        st.session_state["user"] = user
        st.success("Logged in.")
        st.switch_page("app.py")
    else:
        st.error("Invalid email or password.")
st.page_link("pages/signup.py", label="Create a new account")
