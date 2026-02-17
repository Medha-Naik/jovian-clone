from flask import Flask, render_template, jsonify,request
from database import load_jobs_from_db, create_tables, load_job_from_db,save_application_to_db,load_all_applications
from email_service import send_application_confirmation
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



@app.route("/job/<id>/apply", methods=['POST'])
def apply_to_job(id):



    job=load_job_from_db(id)
    if not job:
        return "Job not found",404
    data={
        'job_id':id,
        'full_name':request.form.get('full_name'),
        'email':request.form.get('email'),
        'linkedin': request.form.get('linkedin'),
        'resume': request.form.get('resume'),
        'cover_letter': request.form.get('cover_letter')
    }
    application_id=save_application_to_db(data)
    
    try:
        # Email to applicant
        
        result1=send_application_confirmation(
            applicant_email=data['email'],
            applicant_name=data['full_name'],
            job_title=job['title'],
            application_id=application_id
        )
    except Exception as e:
        print(f"Email error: {str(e)}")
        

    data['application_id']=application_id
    return render_template('application_submitted.html',application=data)


@app.route("/admin/applications")
def admin_applications():
    applications=load_all_applications()
    return render_template("admin_applications.html",applications=applications)

if __name__ == "__main__":
    app.run(debug=True)
