import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section, metric_card
from components.charts import trend_line
from agents.salary_agent import salary_growth, what_if

st.set_page_config(page_title="What-If Simulator | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
section("What-If Salary Simulator", "Model how new skills, certifications, and leadership signals affect compensation.")
base = st.number_input("Current salary", 30000, 500000, 100000, step=5000)
new_skills = st.slider("New high-value skills", 0, 10, 3)
cert = st.checkbox("Add recognized certification")
lead = st.checkbox("Add leadership or ownership proof")
years = st.slider("Future career growth years", 1, 10, 5)
scenario = what_if(base, new_skills, cert, lead)
metric_card("Projected Lift", f"{scenario['lift_percent']}%", f"${scenario['new_salary']:,.0f} target salary")
rows = salary_growth(scenario["new_salary"], scenario["lift_percent"] / 250, years)
st.plotly_chart(trend_line(rows), use_container_width=True)
