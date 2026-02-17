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

        conn.execute(text("""
                          CREATE TABLE IF NOT EXISTS applications(
                          id SERIAL PRIMARY KEY,
                          job_id  INTEGER NOT NULL,
                          full_name VARCHAR(100) NOT NULL,
                          email VARCHAR(100) NOT NULL,
                          phone VARCHAR(20),
                          linkedin VARCHAR(200),
                          resume VARCHAR(200),
                          cover_letter TEXT,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          FOREIGN KEY (job_id) REFERENCES jobs(id))
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

def save_application_to_db(data):
    with engine.begin() as conn:
        result=conn.execute(text(
            """
            INSERT INTO applications
            (job_id, full_name, email, linkedin, resume, cover_letter)
            VALUES
            (:job_id,:full_name,:email,:linkedin,:resume,:cover_letter)
            RETURNING id
"""
        ),data)
        application_id=result.fetchone()[0]
        return application_id
    

def load_application_for_job(job_id):
    with engine.connect() as conn:
        result=conn.execute(
            text("" \
            "SELECT * FROM applications WHERE job_id =:job_id ORDER BY created_at DESC"),
            {"job_id":job_id}
        )
        applications=[]
        for row in result :
            applications.append(dict(row._mapping))
        return applications
    

def load_all_applications():
    with engine.connect() as conn:
        result = conn.execute(text(
            """
            SELECT * FROM applications
"""
        ))
        rows=result.fetchall()
        applications=[]
        for row in rows:
            app_dict=dict(row._mapping)
            applications.append(app_dict)

        return applications