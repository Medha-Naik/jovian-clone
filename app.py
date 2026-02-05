from flask import Flask, render_template, jsonify
from database import load_jobs_from_db,create_tables
from sqlalchemy import text
from database import engine


app = Flask(__name__)

with app.app_context():
    create_tables()


@app.route("/")
def homepage():
    jobs=load_jobs_from_db()
    return render_template("index.html",Jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
    jobs=load_jobs_from_db()
    return jsonify(jobs)

@app.route("/seed")
def seed():
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO jobs (title, location, responsibilities, requirements)
            VALUES
            ('Data Analyst', 'Bengaluru', 'Analyze data and create reports', 'Python, SQL, Excel'),
            ('Data Scientist', 'Delhi', 'Build ML models', 'Python, ML, Statistics'),
            ('Frontend Developer', 'Mumbai', 'Build UI', 'HTML, CSS, JavaScript, React'),
            ('Backend Developer', 'Hyderabad', 'Build APIs', 'Flask, PostgreSQL')
            """))
        return "jobs added succesfully!"



if __name__ =="__main__":
    app.run(debug=True)