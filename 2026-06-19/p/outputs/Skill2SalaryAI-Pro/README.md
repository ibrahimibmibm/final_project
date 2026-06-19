# Skill2Salary AI Pro

A polished browser-based career intelligence app with minimal login, animated background, interactive dashboards, resume skill extraction, salary simulation, roadmap planning, and an AI-style career coach.

## Why This Version

This rebuild focuses on fewer features with stronger impact:

- No confusing signup form
- No Python package installation problems
- Premium animated interface
- Realtime charts and sliders
- Resume analysis in the browser
- Chat-style career coach
- Local data storage in the browser

## How To Run With Python

Run:

```bash
python app.py
```

Then open:

```text
http://localhost:8501/index.html
```

The app uses only Python's built-in web server, so no package installation is required.

## Alternative Direct Open

Open this file directly in your browser:

```text
index.html
```

Or in VS Code:

1. Install the "Live Server" extension.
2. Right-click `index.html`.
3. Click "Open with Live Server".

## Files

```text
Skill2SalaryAI-Pro/
  app.py
  index.html
  assets/
    style.css
    app.js
  README.md
```

## Best Use Flow

1. Enter your name and target role.
2. Open Resume AI.
3. Paste your resume or use the sample.
4. Watch skills, ATS score, salary, radar, roadmap, and coach update.
5. Use Salary Lab sliders for realtime salary simulation.

## Note

The coach runs locally with career-intelligence rules. To connect a real hosted LLM later, add a small backend API and send chat messages there securely.
