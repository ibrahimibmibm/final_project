# Project Summary

## Name

Skill2Salary AI

## Tagline

Transform Skills Into Salary Insights

## What Was Built

A complete modular Streamlit application for AI-powered career intelligence. The app includes authentication, profile management, resume analysis, NLP-based skill extraction, ATS scoring, salary prediction, career scoring, skill-gap analysis, job matching, learning roadmaps, project and certification recommendations, portfolio analysis, interview simulation, market trends, what-if salary modeling, future growth simulation, and PDF report generation.

## Architecture

- `app.py` provides the home screen and profile command center.
- `pages/` contains every Streamlit feature module.
- `database/db.py` owns SQLite setup, persistence, authentication, profile storage, skills, resumes, predictions, reports, and market data.
- `nlp/` handles resume parsing and deterministic skill extraction.
- `ml/` provides a trained scikit-learn salary prediction pipeline using synthetic market data.
- `agents/` contains career, resume, roadmap, and salary advisory logic.
- `components/` contains shared UI, charts, navigation, and theme loading.
- `assets/css/custom.css` creates the dark futuristic glassmorphism interface with animation, glow, hover states, dashboard cards, and responsive styling.

## Production Hardening Ideas

- Add OAuth or enterprise SSO.
- Move SQLite to Postgres for concurrent multi-user deployment.
- Add encrypted password hashing with bcrypt or Argon2.
- Connect live job market APIs.
- Replace deterministic coach responses with an approved LLM service.
- Add unit and browser-based tests.
- Add admin dashboards and audit logging.

## Run Command

```bash
streamlit run app.py
```
