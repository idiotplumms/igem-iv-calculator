from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from functools import wraps
import os

app = Flask(__name__)

# IMPORTANT:
# Set these as environment variables when you deploy.
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-key")

LOGIN_USERNAME = os.environ.get("LOGIN_USERNAME")
LOGIN_PASSWORD = os.environ.get("LOGIN_PASSWORD")


# -------------------------
# Login protection
# -------------------------

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(
                url_for("login", next=request.path)
            )
        return view(*args, **kwargs)

    return wrapped_view


# -------------------------
# Login page
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    # Already logged in
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

            # Remember me
            if remember:
                session.permanent = True

                # Keep the login for 30 days
                app.permanent_session_lifetime = 60 * 60 * 24 * 30

            next_page = request.args.get("next")

            # Basic protection against redirecting to another website
            if next_page and next_page.startswith("/"):
                return redirect(next_page)

            return redirect(url_for("home"))

        return render_template(
            "login.html",
            error="Incorrect username or password."
        )

    return render_template("login.html")


# -------------------------
# Logout
# -------------------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# -------------------------
# Main pages
# -------------------------

@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("slides.html")


@app.route("/Calculator")
@app.route("/calculator")
@login_required
def calculator():
    return render_template("IV_Calc.html")


# -------------------------
# Protected PDF
# -------------------------

@app.route("/briefing.pdf")
@login_required
def briefing_pdf():
    return send_from_directory(
        "files",
        "IGEM_UP1B_Edition4_Engineer_Briefing_FINAL.pdf"
    )


# -------------------------
# Run locally
# -------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
