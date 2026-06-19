import streamlit as st
from components.theme import load_css
from components.navbar import require_auth, sidebar
from components.cards import section
from components.charts import bar
from database.db import table_df

st.set_page_config(page_title="Market Trends | Skill2Salary AI", layout="wide")
load_css(); sidebar()
if not require_auth(): st.stop()
section("Market Trend Dashboard", "Trending skills, salary lift, and demand signals.")
df = table_df("SELECT skill, demand_score, salary_lift, trend FROM market_data ORDER BY demand_score DESC")
st.plotly_chart(bar(df, "skill", "demand_score", "Trending Skills Dashboard"), use_container_width=True)
st.dataframe(df, use_container_width=True, hide_index=True)
