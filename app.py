from flask import Flask, render_template, jsonify
from database import load_jobs_from_db, create_tables, load_job_from_db
from sqlalchemy import text
from database import engine

app = Flask(__name__)

with app.app_context():
    create_tables()


# =========================
# HOMEPAGE
# =========================
@app.route("/")
def homepage():
    jobs = load_jobs_from_db()
    print("HOMEPAGE JOBS:", jobs)
    return render_template("index.html", Jobs=jobs)



# =========================
# API
# =========================
@app.route("/api/jobs")
def list_jobs():
    jobs = load_jobs_from_db()
    return jsonify(jobs)


# =========================
# JOB DETAIL PAGE
# =========================
@app.route("/job/<int:id>")
def show_job(id):
    job = load_job_from_db(id)
    jobs = load_jobs_from_db()

    if not job:
        return "Job not found", 404

    return render_template("jobpage.html", job=job, jobs=jobs)


# =========================
# SEED (SAFE VERSION)
# =========================
@app.route("/seed")
def seed():
    if not app.debug:
        return "Not allowed", 403

    with engine.begin() as conn:
        # Completely clear table + reset ID counter
        conn.execute(text("TRUNCATE TABLE jobs RESTART IDENTITY"))

        # Insert fresh jobs
        conn.execute(text("""
            INSERT INTO jobs (title, location, responsibilities, requirements)
            VALUES
            ('Data Analyst', 'Bengaluru', 'Analyze data and create reports', 'Python, SQL, Excel'),
            ('Data Scientist', 'Delhi', 'Build ML models', 'Python, ML, Statistics'),
            ('Frontend Developer', 'Mumbai', 'Build UI', 'HTML, CSS, JavaScript, React'),
            ('Backend Developer', 'Hyderabad', 'Build APIs', 'Flask, PostgreSQL')
        """))

    return "Database reseeded cleanly!"


# =========================
# RESET DATABASE
# =========================
@app.route("/reset")
def reset():
    if not app.debug:
        return "Not allowed", 403

    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS jobs CASCADE"))
        create_tables()

    return "Database fully reset!"


if __name__ == "__main__":
    app.run(debug=True)
