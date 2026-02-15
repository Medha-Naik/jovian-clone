import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)


def create_tables():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                title VARCHAR(250),
                location VARCHAR(250),
                responsibilities VARCHAR(2000),
                requirements VARCHAR(2000)
            )
        """))


def insert_job(title, location, responsibilities, requirements):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO jobs (title, location, responsibilities, requirements)
            VALUES (:title, :location, :responsibilities, :requirements)
        """), {
            "title": title,
            "location": location,
            "responsibilities": responsibilities,
            "requirements": requirements
        })


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        return [dict(row._mapping) for row in result]


def load_job_from_db(job_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM jobs WHERE id = :id"),
            {"id": job_id}
        )
        row = result.fetchone()
        return dict(row._mapping) if row else None
