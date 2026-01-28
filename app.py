from flask import Flask, render_template, jsonify

app = Flask(__name__)





Jobs=[
    {
       'id':1,
       'title':"Data Analysst",
       'location': 'Bengaluru, India'
    },
    {
        'id':2,
        'title':"SDE1",
        'location':'Bengaluru, India'
    },
    {
        'id':3,
        'title':"Data Scientist",
        'location':'Delhi, India'
    },
    {
        'id':3,
        'title':"Backend Engineer",
        'location':'San Francisco, USA'
    }
]

@app.route("/")
def homepage():
    return render_template("index.html",Jobs=Jobs)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(Jobs)


if __name__ =="__main__":
    app.run(debug=True)