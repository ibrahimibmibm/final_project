from ml.salary_model import training_frame


def export_training_data(path: str = "synthetic_salary_training.csv") -> str:
    df = training_frame()
    df.to_csv(path, index=False)
    return path
