import hashlib
import hmac
import json
import logging
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "skill2salary.db"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("skill2salary")


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        logger.exception("Database transaction failed")
        raise
    finally:
        conn.close()


def password_hash(password: str, salt: bytes | None = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 120_000)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    if "$" not in stored:
        return hashlib.sha256(password.encode("utf-8")).hexdigest() == stored
    salt_hex, digest_hex = stored.split("$", 1)
    candidate = password_hash(password, bytes.fromhex(salt_hex)).split("$", 1)[1]
    return hmac.compare_digest(candidate, digest_hex)


def init_db() -> None:
    schema = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        title TEXT DEFAULT '',
        target_role TEXT DEFAULT '',
        experience INTEGER DEFAULT 0,
        location TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT,
        text TEXT,
        ats_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        skill TEXT,
        category TEXT,
        confidence REAL DEFAULT 1.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS salary_predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        predicted_salary REAL,
        confidence REAL,
        inputs TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS career_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        health_score REAL,
        success_probability REAL,
        details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        target_role TEXT,
        weekly_plan TEXT,
        monthly_plan TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS job_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        company TEXT,
        match_score REAL,
        missing_skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        question TEXT,
        answer TEXT,
        feedback TEXT,
        score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS market_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill TEXT,
        demand_score REAL,
        salary_lift REAL,
        trend TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS portfolio_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        source TEXT,
        score REAL,
        findings TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        file_path TEXT,
        summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with get_connection() as conn:
        conn.executescript(schema)
        seed_market_data(conn)


def seed_market_data(conn: sqlite3.Connection) -> None:
    count = conn.execute("SELECT COUNT(*) FROM market_data").fetchone()[0]
    if count:
        return
    rows = [
        ("Python", 94, 0.10, "Rising"), ("Machine Learning", 92, 0.18, "Rising"),
        ("SQL", 88, 0.08, "Stable"), ("Cloud", 90, 0.14, "Rising"),
        ("React", 82, 0.09, "Stable"), ("NLP", 84, 0.15, "Rising"),
        ("MLOps", 87, 0.19, "Rising"), ("Data Visualization", 79, 0.07, "Stable"),
        ("Docker", 81, 0.08, "Stable"), ("Generative AI", 95, 0.22, "Rising"),
    ]
    conn.executemany("INSERT INTO market_data(skill, demand_score, salary_lift, trend) VALUES (?, ?, ?, ?)", rows)


def create_user(name: str, email: str, password: str, title: str = "", target_role: str = "", experience: int = 0, location: str = "") -> bool:
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users(name, email, password_hash, title, target_role, experience, location) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name.strip(), email.lower().strip(), password_hash(password), title, target_role, int(experience), location),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def authenticate(email: str, password: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE email=?", (email.lower().strip(),)).fetchone()
        if row and verify_password(password, row["password_hash"]):
            return dict(row)
        return None


def get_user(user_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        return dict(row) if row else None


def update_user(user_id: int, **fields: Any) -> None:
    allowed = {"name", "title", "target_role", "experience", "location"}
    clean = {k: v for k, v in fields.items() if k in allowed}
    if not clean:
        return
    assignments = ", ".join(f"{key}=?" for key in clean)
    with get_connection() as conn:
        conn.execute(f"UPDATE users SET {assignments} WHERE id=?", (*clean.values(), user_id))


def save_resume(user_id: int, filename: str, text: str, ats_score: float) -> None:
    with get_connection() as conn:
        conn.execute("INSERT INTO resumes(user_id, filename, text, ats_score) VALUES (?, ?, ?, ?)", (user_id, filename, text, ats_score))


def save_skills(user_id: int, skills: list[str], category: str = "Technical") -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM skills WHERE user_id=?", (user_id,))
        conn.executemany("INSERT INTO skills(user_id, skill, category) VALUES (?, ?, ?)", [(user_id, s, category) for s in sorted(set(skills))])


def fetch_user_skills(user_id: int) -> list[str]:
    with get_connection() as conn:
        return [row["skill"] for row in conn.execute("SELECT skill FROM skills WHERE user_id=? ORDER BY skill", (user_id,))]


def latest_resume(user_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM resumes WHERE user_id=? ORDER BY created_at DESC, id DESC LIMIT 1", (user_id,)).fetchone()
        return dict(row) if row else None


def save_json(table: str, user_id: int, data: dict[str, Any]) -> None:
    with get_connection() as conn:
        if table == "salary_predictions":
            conn.execute("INSERT INTO salary_predictions(user_id, role, predicted_salary, confidence, inputs) VALUES (?, ?, ?, ?, ?)",
                         (user_id, data["role"], data["predicted_salary"], data["confidence"], json.dumps(data.get("inputs", {}))))
        elif table == "career_scores":
            conn.execute("INSERT INTO career_scores(user_id, health_score, success_probability, details) VALUES (?, ?, ?, ?)",
                         (user_id, data["health_score"], data["success_probability"], json.dumps(data)))
        elif table == "portfolio_analysis":
            conn.execute("INSERT INTO portfolio_analysis(user_id, source, score, findings) VALUES (?, ?, ?, ?)",
                         (user_id, data["source"], data["score"], json.dumps(data)))


def table_df(query: str, params: tuple[Any, ...] = ()):
    import pandas as pd
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)
