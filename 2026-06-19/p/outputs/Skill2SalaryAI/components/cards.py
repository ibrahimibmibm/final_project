import streamlit as st


def metric_card(title: str, value: str, caption: str = "") -> None:
    st.markdown(
        f"""
        <div class="glass-card metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='section-title'>{title}</div><div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def tag_cloud(items: list[str]) -> None:
    html = "".join(f"<span class='skill-pill'>{item}</span>" for item in items)
    st.markdown(f"<div class='tag-cloud'>{html}</div>", unsafe_allow_html=True)
