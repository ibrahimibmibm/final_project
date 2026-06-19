def salary_growth(current_salary: float, skill_lift: float, years: int) -> list[dict]:
    rows = []
    salary = current_salary
    for year in range(1, years + 1):
        salary *= 1.04 + skill_lift
        rows.append({"year": year, "projected_salary": round(salary, 2)})
    return rows


def what_if(base_salary: float, new_skills: int, certification: bool, leadership: bool) -> dict:
    lift = new_skills * 0.025 + (0.06 if certification else 0) + (0.08 if leadership else 0)
    return {"lift_percent": round(lift * 100, 1), "new_salary": round(base_salary * (1 + lift), 2)}
