# Skill2Salary AI

Transform Skills Into Salary Insights.

Skill2Salary AI is a Streamlit-based career intelligence platform with authentication, resume parsing, skill extraction, salary prediction, career scoring, job matching, portfolio analysis, interview practice, market trends, simulations, and downloadable PDF reports.

## Features

- Signup, login, logout, and session management
- User profile management
- Resume upload, parsing, skill extraction, and ATS score
- Career health score and success probability
- Salary prediction with confidence and range
- Skill gap analysis for target roles
- Career path explorer
- Personalized weekly and monthly learning roadmaps
- Project and certification recommendations
- Job match engine
- Portfolio and GitHub signal analyzer
- AI career coach chat interface
- Interview simulator
- Market trend and trending skills dashboard
- What-if salary and future growth simulator
- Downloadable AI career report PDF

## Project Structure

```text
Skill2SalaryAI/
  app.py
  pages/
  database/
  ml/
  nlp/
  agents/
  components/
  assets/
  uploads/
  reports/
  requirements.txt
  README.md
  PROJECT_SUMMARY.md
```

## Database Schema

SQLite database tables are created automatically in `skill2salary.db`:

- `users`
- `resumes`
- `skills`
- `salary_predictions`
- `career_scores`
- `roadmaps`
- `job_matches`
- `interviews`
- `market_data`
- `portfolio_analysis`
- `reports`
- `chat_history`

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Optional spaCy model:

```bash
python -m spacy download en_core_web_sm
```

The current extractor uses a deterministic skill catalog, so the app runs even without the optional spaCy model.

## Run

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit.

## Testing

```bash
python -m compileall .
python -m ml.training
```

Recommended manual checks:

- Create an account
- Upload a PDF or TXT resume
- Confirm skills and ATS score appear
- Run salary prediction
- Open dashboard, skill gap, roadmap, market trends, simulator, and report pages
- Generate and download the PDF report

## Deployment

For Streamlit Community Cloud, deploy this folder and set the main file to `app.py`.

For a VM or container:

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

Use persistent storage for `skill2salary.db`, `uploads/`, and `reports/` in production.

## Notes

This project uses local deterministic AI-style agents and a synthetic salary model so it can run without external APIs. Replace or extend the agents with hosted LLM calls when you want live generative responses.
