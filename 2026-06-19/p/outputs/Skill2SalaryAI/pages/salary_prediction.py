import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import metric_card, section
from components.charts import salary_range
from database.db import fetch_user_skills, save_json
from ml.salary_model import predict_salary

st.set_page_config(page_title="Salary Prediction | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
user = st.session_state["user"]
skills = fetch_user_skills(user["id"])
section("Salary Prediction", "Estimate salary, confidence, and range from role, experience, location, and skill depth.")
role = st.selectbox("Role", ["AI Engineer", "ML Engineer", "Data Scientist", "Data Analyst", "Full-Stack Developer", "Product Manager"], index=0)
experience = st.slider("Experience", 0, 30, int(user.get("experience") or 2))
location = st.selectbox("Location", ["Remote", "New York", "San Francisco", "Austin", "Chicago", "Boston"])
skill_count = st.slider("Skill count", 0, 30, len(skills))
if st.button("Predict salary", use_container_width=True):
    result = predict_salary(role, experience, skill_count, location)
    save_json("salary_predictions", user["id"], {"role": role, "predicted_salary": result.predicted_salary, "confidence": result.confidence, "inputs": {"experience": experience, "skills": skill_count, "location": location}})
    c1, c2 = st.columns(2)
    with c1:
        metric_card("Predicted Salary", f"${result.predicted_salary:,.0f}", f"{result.confidence}% confidence")
    with c2:
        st.plotly_chart(salary_range(result.low, result.predicted_salary, result.high), use_container_width=True)
