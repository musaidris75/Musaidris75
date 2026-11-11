"""
CSC 312 - Web Application Development (Tutor-Marked Assessment)
StudyHub: a simple Flask signup app with MySQL.

  1. Setup            - Flask is created in this file
  2. Homepage         - templates/index.html (HTML + Bootstrap)
  3. Signup page      - templates/signup.html, checked with request.form
  4. Database         - MySQL table tbl_user (schema.sql), via mysql-connector-python
  5. Password safety  - the password is hashed before it is saved

Run:  python app.py   then open http://127.0.0.1:5000
"""
import os

import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

# 1. Setup: create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "studyhub-secret-key")

# MySQL login details (change these or set them as environment variables)
db_config = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", "3306")),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DB", "studyhub_db"),
}


# 4. Database integration: connect Flask to MySQL
def get_db():
    return mysql.connector.connect(**db_config)


# 2. Homepage
@app.route("/")
def home():
    return render_template("index.html")


# 3. Signup page
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Read the form data with request.form
        username = request.form["username"].strip()
        password = request.form["password"]
        confirm = request.form["confirm"]

        # Validate the form data
        error = None
        if not username or not password:
            error = "Please fill in both username and password."
        elif len(username) < 4 or len(username) > 30:
            error = "Username must be between 4 and 30 characters."
        elif not username.replace("_", "").isalnum():
            error = "Username can only contain letters, numbers and underscores."
        elif len(password) < 8:
            error = "Password must be at least 8 characters."
        elif password != confirm:
            error = "Passwords do not match."

        if error:
            flash(error, "danger")
            return render_template("signup.html", username=username)

        # 5. Password security: hash the password before saving it
        hashed = generate_password_hash(password, method="pbkdf2:sha256")

        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tbl_user (username, password) VALUES (%s, %s)",
                (username, hashed),
            )
            conn.commit()
            cur.close()
            conn.close()
        except mysql.connector.IntegrityError:
            flash("This username is already taken.", "danger")
            return render_template("signup.html", username=username)
        except mysql.connector.Error as err:
            print("MySQL error:", err)
            flash("Could not connect to the database.", "danger")
            return render_template("signup.html", username=username)

        flash("Signup successful! Your account has been created.", "success")
        return redirect(url_for("home"))

    return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)
