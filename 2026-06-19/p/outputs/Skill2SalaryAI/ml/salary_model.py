from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


@dataclass
class SalaryResult:
    role: str
    predicted_salary: float
    confidence: float
    low: float
    high: float


def training_frame() -> pd.DataFrame:
    roles = ["Data Analyst", "Data Scientist", "ML Engineer", "AI Engineer", "Full-Stack Developer", "Product Manager"]
    locations = ["Remote", "New York", "San Francisco", "Austin", "Chicago", "Boston"]
    rows = []
    rng = np.random.default_rng(42)
    base = {"Data Analyst": 78000, "Data Scientist": 118000, "ML Engineer": 135000, "AI Engineer": 148000, "Full-Stack Developer": 112000, "Product Manager": 126000}
    for role in roles:
        for exp in range(0, 16):
            for skills in range(3, 19, 3):
                loc = rng.choice(locations)
                loc_lift = {"San Francisco": 28000, "New York": 18000, "Boston": 13000, "Austin": 9000, "Chicago": 7000, "Remote": 4000}[loc]
                salary = base[role] + exp * 5200 + skills * 1700 + loc_lift + rng.normal(0, 5500)
                rows.append({"role": role, "experience": exp, "skill_count": skills, "location": loc, "salary": max(50000, salary)})
    return pd.DataFrame(rows)


def build_model() -> Pipeline:
    df = training_frame()
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["role", "location"])], remainder="passthrough")
    model = Pipeline([("pre", pre), ("rf", RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=2))])
    model.fit(df[["role", "experience", "skill_count", "location"]], df["salary"])
    return model


MODEL = build_model()


def predict_salary(role: str, experience: int, skill_count: int, location: str) -> SalaryResult:
    X = pd.DataFrame([{"role": role, "experience": experience, "skill_count": skill_count, "location": location}])
    pred = float(MODEL.predict(X)[0])
    confidence = min(94, 58 + skill_count * 2 + min(experience, 10) * 2)
    spread = pred * (1 - confidence / 130)
    return SalaryResult(role, round(pred, 2), round(confidence, 1), round(pred - spread, 2), round(pred + spread, 2))
