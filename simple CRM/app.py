from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("leads.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            message TEXT,
            status TEXT DEFAULT 'New'
        )
    """)
    conn.commit()
    conn.close()

create_table()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        conn = get_db()
        conn.execute(
            "INSERT INTO leads (name, email, phone, message) VALUES (?, ?, ?, ?)",
            (name, email, phone, message)
        )
        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    leads = conn.execute("SELECT * FROM leads ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("dashboard.html", leads=leads)

@app.route("/update/<int:id>/<status>")
def update_status(id, status):
    conn = get_db()
    conn.execute("UPDATE leads SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)
