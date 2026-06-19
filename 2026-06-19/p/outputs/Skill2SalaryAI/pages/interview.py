import random
import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section, metric_card

QUESTIONS = {
    "AI Engineer": ["How would you design an LLM-powered support assistant?", "How do you evaluate hallucination risk?"],
    "ML Engineer": ["How would you monitor model drift?", "Explain your approach to feature stores."],
    "Data Scientist": ["How do you validate a model before launch?", "Describe an experiment you would run."],
}

st.set_page_config(page_title="Interview | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
section("Interview Simulator", "Practice role-specific answers and get structured feedback.")
role = st.selectbox("Interview role", list(QUESTIONS))
question = st.selectbox("Question", QUESTIONS[role], index=random.randrange(len(QUESTIONS[role])))
answer = st.text_area("Your answer", height=180)
if st.button("Evaluate answer", use_container_width=True):
    score = min(100, 30 + len(answer.split()) * 2 + (15 if any(x in answer.lower() for x in ["metric", "tradeoff", "monitor", "user"]) else 0))
    metric_card("Interview Score", f"{score}%", "Structure, specificity, and impact")
    st.write("Feedback: add a concise situation, your technical decision, tradeoffs, metrics, and the final result.")
