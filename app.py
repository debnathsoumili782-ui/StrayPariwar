from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "straypariwar_secret"

DATABASE = "database.db"


# =========================
# DATABASE AUTO CREATE
# =========================
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


init_db()


# =========================
# ROUTES
# =========================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, password))
            conn.commit()
            flash("Registration Successful! Please login.")
            return redirect(url_for("login"))
        except:
            flash("Email already exists!")
        finally:
            conn.close()

    return render_template("register.html")


# =========================
# LOGIN
# =========================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                       (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["username"] = user[1]
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials!")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


# =========================
# ADOPTION
# =========================
@app.route("/adoption", methods=["GET", "POST"])
def adoption():
    message = None
    if request.method == "POST":
        message = "Adoption request submitted successfully! 🐾"

    return render_template("adoption.html", message=message)
@app.route("/join")
def join():
    if "username" in session:
        return redirect(url_for("services"))  # login thakle services e jabe
    else:
        return redirect(url_for("register"))  # login na thakle register e jabe
@app.route("/feeding")
def feeding():
    return render_template("feeding.html")

@app.route("/rescuing")
def rescuing():
    return render_template("rescuing.html")

@app.route("/grooming")
def grooming():
    return render_template("grooming.html")

@app.route("/submit_adoption", methods=["POST"])
def submit_adoption():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    address = request.form.get("address")

    # Future e DB save korte parba ekhane

    return render_template("success.html", name=name)

@app.route("/ngos")
def ngos():
    return render_template("ngos.html")


if __name__ == "__main__":
    app.run(debug=True)
