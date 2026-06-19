import streamlit as st

from database.db import init_db, update_user
from components.navbar import sidebar
from components.cards import metric_card, section
from components.theme import load_css


st.set_page_config(page_title="Skill2Salary AI", page_icon="S2S", layout="wide")
init_db()
load_css()
sidebar()

st.markdown(
    """
    <div class="hero">
      <h1>Skill2Salary AI</h1>
      <p>Transform Skills Into Salary Insights</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "user" not in st.session_state:
    st.info("Create an account or log in to unlock your career intelligence workspace.")
    c1, c2 = st.columns(2)
    c1.page_link("pages/login.py", label="Login", icon=":material/login:")
    c2.page_link("pages/signup.py", label="Sign up", icon=":material/person_add:")
else:
    user = st.session_state["user"]
    section("Career Command Center", "Keep your profile current for stronger predictions.")
    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Current Role", user.get("title") or "Not set", "Used for salary context")
    with c2:
        metric_card("Target Role", user.get("target_role") or "Not set", "Used for skill-gap analysis")
    with c3:
        metric_card("Experience", f"{user.get('experience', 0)} yrs", "Used by growth models")

    with st.expander("Update profile", expanded=False):
        name = st.text_input("Name", value=user.get("name", ""))
        title = st.text_input("Current title", value=user.get("title", ""))
        target_role = st.selectbox(
            "Target role",
            ["AI Engineer", "ML Engineer", "Data Scientist", "Data Analyst", "Full-Stack Developer", "Product Manager"],
            index=["AI Engineer", "ML Engineer", "Data Scientist", "Data Analyst", "Full-Stack Developer", "Product Manager"].index(user.get("target_role") or "AI Engineer")
            if (user.get("target_role") or "AI Engineer") in ["AI Engineer", "ML Engineer", "Data Scientist", "Data Analyst", "Full-Stack Developer", "Product Manager"] else 0,
        )
        experience = st.number_input("Years of experience", min_value=0, max_value=40, value=int(user.get("experience") or 0))
        location = st.text_input("Location", value=user.get("location") or "Remote")
        if st.button("Save profile"):
            update_user(user["id"], name=name, title=title, target_role=target_role, experience=experience, location=location)
            st.session_state["user"].update({"name": name, "title": title, "target_role": target_role, "experience": experience, "location": location})
            st.success("Profile updated.")

    st.subheader("Launch a module")
    cols = st.columns(4)
    links = [
        ("Dashboard", "pages/dashboard.py", ":material/dashboard:"),
        ("Resume Analyzer", "pages/resume_analyzer.py", ":material/upload_file:"),
        ("Salary Prediction", "pages/salary_prediction.py", ":material/payments:"),
        ("Career Report", "pages/career_report.py", ":material/picture_as_pdf:"),
    ]
    for col, (label, page, icon) in zip(cols, links):
        col.page_link(page, label=label, icon=icon)
