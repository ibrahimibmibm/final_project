import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PLOTLY_TEMPLATE = "plotly_dark"


def gauge(value: float, title: str):
    return go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title},
        gauge={"axis": {"range": [0, 100]}, "bar": {"color": "#8B5CF6"}, "bgcolor": "#121212"},
    )).update_layout(template=PLOTLY_TEMPLATE, height=260, margin=dict(l=20, r=20, t=50, b=20))


def salary_range(low: float, mid: float, high: float):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=["Low", "Prediction", "High"], y=[low, mid, high], marker_color=["#06B6D4", "#8B5CF6", "#3B82F6"]))
    return fig.update_layout(template=PLOTLY_TEMPLATE, height=320, yaxis_title="USD")


def trend_line(rows: list[dict]):
    df = pd.DataFrame(rows)
    return px.line(df, x="year", y="projected_salary", markers=True, template=PLOTLY_TEMPLATE).update_traces(line_color="#06B6D4")


def bar(df: pd.DataFrame, x: str, y: str, title: str):
    return px.bar(df, x=x, y=y, title=title, template=PLOTLY_TEMPLATE, color=y, color_continuous_scale=["#06B6D4", "#8B5CF6"])
