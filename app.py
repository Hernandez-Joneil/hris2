from flask import Flask, render_template, request, redirect, session
from flask_pymysql import MySQL
import config
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", "secretkey")

app.config["MYSQL_HOST"] = config.MYSQL_HOST
app.config["MYSQL_USER"] = config.MYSQL_USER
app.config["MYSQL_PASSWORD"] = config.MYSQL_PASSWORD
app.config["MYSQL_DB"] = config.MYSQL_DB
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("applicant_apply.html")

@app.route("/exam_portal")
def exam_portal():
    return render_template("applicant_exam_login.html")


@app.route("/apply", methods=["POST"])
def apply():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    address = request.form["address"]

    resume = request.files["resume"]

    filename = secure_filename(resume.filename)

    resume.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    cur = mysql.connection.cursor()

    cur.execute(
    "INSERT INTO applicants(name,email,phone,address,resume,status) VALUES(%s,%s,%s,%s,%s,%s)",
    (name,email,phone,address,filename,"Pending")
    )

    mysql.connection.commit()

    return "Application Submitted"


@app.route("/hr_login", methods=["GET","POST"])
def hr_login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute(
        "SELECT * FROM hr_users WHERE email=%s AND password=%s",
        (email,password)
        )

        user = cur.fetchone()

        if user:
            session["hr"] = user[1]
            return redirect("/dashboard")
        else:
            return render_template("hr_login.html", error="Invalid credentials")

    return render_template("hr_login.html")


@app.route("/dashboard")
def dashboard():
    if "hr" not in session:
        return redirect("/hr_login")

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT applicants.id, applicants.name, applicants.email,
        applicants.status, applicants.resume
        FROM applicants
    """)
    applicants = cur.fetchall()
    return render_template("hr_dashboard.html", applicants=applicants)

@app.route("/create_exam", methods=["GET","POST"])
def create_exam():

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        code = request.form["code"]

        cur = mysql.connection.cursor()

        cur.execute(
        "INSERT INTO exams(title,description,exam_code) VALUES(%s,%s,%s)",
        (title,description,code)
        )

        mysql.connection.commit()

        return redirect("/dashboard")

    return render_template("create_exam.html")


@app.route("/schedule_exam", methods=["GET","POST"])
def schedule_exam():

    cur = mysql.connection.cursor()

    if request.method == "POST":

        applicant = request.form["applicant_id"]
        exam = request.form["exam_id"]
        date = request.form["date"]  # Fixed: Changed from "exam_date" to "date" to match form

        cur.execute(
        "INSERT INTO exam_schedule(applicant_id,exam_id,exam_date) VALUES(%s,%s,%s)",
        (applicant,exam,date)
        )

        mysql.connection.commit()

        return redirect("/dashboard")

    cur.execute("SELECT * FROM applicants")
    applicants = cur.fetchall()

    cur.execute("SELECT * FROM exams")
    exams = cur.fetchall()

    return render_template(
        "schedule_exam.html",
        applicants=applicants,
        exams=exams
    )




@app.route("/exam_login", methods=["POST"])

def exam_login():

    email = request.form["email"]
    code = request.form["code"]

    cur = mysql.connection.cursor()

    cur.execute(
    """
    SELECT applicants.name, exams.title
    FROM applicants
    INNER JOIN exam_schedule ON applicants.id = exam_schedule.applicant_id
    INNER JOIN exams ON exams.id = exam_schedule.exam_id
    WHERE applicants.email=%s AND exams.exam_code=%s
    """,
    (email,code)
    )

    data = cur.fetchone()

    if data:
       return redirect("/exam")


    return "Invalid Code"


@app.route("/exam")
def exam():
    return render_template("exam_page.html")

@app.route("/submit_exam", methods=["POST"])
def submit_exam():

    score = 0

    if request.form["q1"] == "a":
        score += 1

    if request.form["q2"] == "a":
        score += 1

    if request.form["q3"] == "b":
        score += 1

    if request.form["q4"] == "b":
        score += 1

    if request.form["q5"] == "a":
        score += 1

    result = "Passed" if score >= 3 else "Failed"

    cur = mysql.connection.cursor()

    # Note: Hardcoded applicant_id=1; replace with session or form data for real use
    cur.execute(
    "INSERT INTO exam_results(applicant_id,score,result) VALUES(%s,%s,%s)",
    (1,score,result)
    )

    mysql.connection.commit()

    return f"Your Score: {score}/5 - {result}"



@app.route("/application_status", methods=["GET","POST"])
def application_status():

    status = None

    if request.method == "POST":

        email = request.form["email"]

        cur = mysql.connection.cursor()

        cur.execute(
        "SELECT status FROM applicants WHERE email=%s",
        (email,)
        )

        result = cur.fetchone()

        if result:
            status = result[0]
        else:
            status = "Application not found"

    return render_template("application_status.html", status=status)


@app.route("/logout")

def logout():
    session.clear()
    return redirect("/")


@app.route("/update_status/<id>/<status>")
def update_status(id,status):

    cur = mysql.connection.cursor()

    cur.execute(
    "UPDATE applicants SET status=%s WHERE id=%s",
    (status,id)
    )

    mysql.connection.commit()

    return redirect("/dashboard")


@app.route("/delete_applicant/<id>")
def delete_applicant(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM applicants WHERE id=%s",(id,))

    mysql.connection.commit()

    return redirect("/dashboard")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)