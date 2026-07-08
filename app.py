from re import search

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        conn.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email)
        )
        conn.commit()
        return redirect("/")

    search = request.args.get("search", "")

    if search:
        users = conn.execute(
        "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
        (f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
     users = conn.execute(
        "SELECT * FROM users"
    ).fetchall()
    
    conn.close()
    return render_template("index.html", users=users)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()

    conn.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        conn.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, id)
        )
        conn.commit()
        conn.close()

        return redirect("/")

    conn.close()
    return render_template("edit.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)

