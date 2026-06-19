import streamlit as st

PAGES = {
    "Dashboard": "pages/dashboard.py",
    "Resume Analyzer": "pages/resume_analyzer.py",
    "Salary Prediction": "pages/salary_prediction.py",
    "Career Score": "pages/career_score.py",
    "Skill Gap": "pages/skill_gap.py",
    "Roadmap": "pages/roadmap.py",
    "Job Match": "pages/job_match.py",
    "Portfolio": "pages/portfolio.py",
    "Interview": "pages/interview.py",
    "Career Coach": "pages/career_coach.py",
    "Market Trends": "pages/market_trends.py",
    "What-If Simulator": "pages/what_if_simulator.py",
    "Career Report": "pages/career_report.py",
}


def require_auth() -> bool:
    if "user" not in st.session_state:
        st.warning("Please log in or create an account to continue.")
        st.page_link("pages/login.py", label="Login")
        st.page_link("pages/signup.py", label="Sign up")
        return False
    return True


def sidebar() -> None:
    user = st.session_state.get("user")
    with st.sidebar:
        st.markdown("<div class='brand'>Skill2Salary AI</div><div class='tagline'>Transform Skills Into Salary Insights</div>", unsafe_allow_html=True)
        if user:
            st.success(f"Signed in as {user['name']}")
            if st.button("Logout", use_container_width=True):
                st.session_state.pop("user", None)
                st.rerun()
        else:
            st.page_link("pages/login.py", label="Login")
            st.page_link("pages/signup.py", label="Sign up")
