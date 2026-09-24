from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from datetime import timedelta
import os

app = Flask(__name__)

app.secret_key = os.environ.get(
"SECRET_KEY",
"change-this-secret-key"
)

LOGIN_USERNAME = os.environ.get("LOGIN_USERNAME",)

LOGIN_PASSWORD = os.environ.get("LOGIN_PASSWORD",)

# =========================

# LOGIN

# =========================

@app.route("/login", methods=["GET", "POST"])
def login():


    if session.get("logged_in"):
        return redirect(url_for("home"))

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:

            session.clear()

            session["logged_in"] = True
            session["username"] = username

            if remember:

                session.permanent = True

                app.permanent_session_lifetime = timedelta(
                    days=30
                )

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Incorrect username or password."
        )

    return render_template("login.html")


# =========================

# LOGOUT

# =========================

@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("login"))


# =========================

# HOME / ENGINEER BRIEFING

# =========================

@app.route("/")
@app.route("/home")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("slides.html")


# =========================

# CALCULATOR

# =========================

@app.route("/Calculator")
@app.route("/calculator")
def calculator():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("IV_Calc.html")


# =========================

# PDF VIEWER PAGE

# =========================

@app.route("/pdf-viewer")
def pdf_viewer():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return render_template("pdf.html")


# =========================

# SERVICE WORKER

# =========================

@app.route("/service-worker.js")
def service_worker():
    return send_from_directory(
        "static",
        "service-worker.js",
        mimetype="application/javascript"
)


# =========================

# PDF FILE

# =========================

@app.route("/briefing.pdf")
def briefing_pdf():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    return send_from_directory(
        "files",
        "IGEM_UP1B_Edition4_Engineer_Briefing_FINAL.pdf",
        mimetype="application/pdf",
        as_attachment=False
    )


# =========================

# START APPLICATION

# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)

