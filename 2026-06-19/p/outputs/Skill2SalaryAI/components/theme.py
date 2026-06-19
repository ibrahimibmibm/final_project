from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]


def load_css() -> None:
    css = BASE_DIR / "assets" / "css" / "custom.css"
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
