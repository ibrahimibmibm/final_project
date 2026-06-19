import re
import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section, metric_card
from database.db import save_json

st.set_page_config(page_title="Portfolio | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
section("Portfolio Analyzer", "Analyze portfolio or GitHub links for project depth, clarity, and hiring signal.")
url = st.text_input("Portfolio or GitHub URL")
description = st.text_area("Paste project descriptions, README text, or portfolio summary")
if st.button("Analyze portfolio", use_container_width=True):
    text = f"{url} {description}".lower()
    signals = ["github", "demo", "metrics", "architecture", "readme", "api", "model", "dashboard", "deployment"]
    hits = [s for s in signals if re.search(s, text)]
    score = min(100, 35 + len(hits) * 8 + (15 if url else 0))
    findings = {"source": url or "manual", "score": score, "strengths": hits, "next_steps": ["Add measurable impact", "Document architecture", "Include a live demo or screenshots"]}
    save_json("portfolio_analysis", st.session_state["user"]["id"], findings)
    metric_card("Portfolio Score", f"{score}%", "Hiring signal strength")
    st.json(findings)
