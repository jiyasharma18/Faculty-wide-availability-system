from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
def get_db():
    return sqlite3.connect("faculty.db")


# ---------- HOME PAGE (VIEW ALL FACULTY) ----------
@app.route('/')
def home():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM faculty_status")
    data = cursor.fetchall()
    conn.close()
    return render_template("index.html", faculty=data)


# ---------- FACULTY LOGIN PAGE ----------
@app.route('/login')
def login():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM faculty_status")
    faculty = cursor.fetchall()
    conn.close()
    return render_template("login.html", faculty=faculty)


# ---------- UPDATE STATUS ----------
@app.route('/update', methods=['POST'])
def update():
    faculty_id = request.form['id']
    status = request.form['status']
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE faculty_status SET status=?, last_seen=? WHERE id=?",
        (status, time, faculty_id)
    )
    conn.commit()
    conn.close()

    return redirect('/')


# ---------- ADD FACULTY PAGE ----------
@app.route('/add')
def add_page():
    return render_template("add.html")


# ---------- ADD FACULTY TO DATABASE ----------
@app.route('/add_faculty', methods=['POST'])
def add_faculty():
    name = request.form['name']
    dept = request.form['department']
    cabin = request.form['cabin']

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO faculty_status (name, department, cabin, status, last_seen) VALUES (?, ?, ?, ?, ?)",
        (name, dept, cabin, "Not Present", "-")
    )
    conn.commit()
    conn.close()

    return redirect('/')


# ---------- RUN SERVER ----------
if __name__ == '__main__':
    app.run(debug=True)