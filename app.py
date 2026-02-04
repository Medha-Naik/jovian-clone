from flask import Flask, render_template, jsonify
from database import load_jobs_from_db
from sqlalchemy import text





app = Flask(__name__)


@app.route("/")
def homepage():
    jobs=load_jobs_from_db()
    return render_template("index.html",Jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
    jobs=load_jobs_from_db()
    return jsonify(jobs)


if __name__ =="__main__":
    app.run(debug=True)