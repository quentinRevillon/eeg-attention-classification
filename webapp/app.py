"""Flask web app running the attention and memory tests and storing the results.

    cd webapp
    python app.py            # then open http://127.0.0.1:5000

Results are written to webapp/instance/attention.db (created on first run).
Set the SECRET_KEY environment variable outside local testing.
"""
import os
from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, redirect, render_template, request, send_from_directory, session, url_for
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from models import BallResult, Result, ResultPrisha1, ResultPrisha2, User, db

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///attention.db"
db.init_app(app)
with app.app_context():
    db.create_all()

SAVED = {"message": "Les résultats ont été enregistrés avec succès."}


def login_required(view):
    """Render the login page instead of ``view`` when no user is logged in."""

    @wraps(view)
    def protected(*args, **kwargs):
        if "email" not in session:
            return render_template("login.html")
        return view(*args, **kwargs)

    return protected


def check_password(email, password):
    """Return True if ``email`` exists and ``password`` matches its hash."""
    user = User.query.filter_by(email=email).first()
    return user is not None and check_password_hash(user.password, password)


def email_exists(email):
    """Return True if an account uses ``email``."""
    return User.query.filter_by(email=email).first() is not None


def next_session_id(model, email, **filters):
    """Return 1 + the largest sessionId of ``email`` in ``model`` (1 for a first session)."""
    last = db.session.query(func.max(model.sessionId)).filter_by(email=email, **filters).scalar()
    return 1 if last is None else last + 1


def today():
    """Return today's date as dd/mm/yyyy."""
    return datetime.now().strftime("%d/%m/%Y")


def save(row):
    """Insert ``row`` and commit."""
    db.session.add(row)
    db.session.commit()


@app.route("/signup", methods=["POST"])
def signup():
    """Create an account and log it in."""
    email, password = request.form["email"], request.form["password"]
    if email_exists(email):
        return "Erreur : email déjà utilisé"
    save(User(email=email, password=generate_password_hash(password, method="pbkdf2:sha256")))
    session["email"] = email
    return redirect(url_for("testSelectionPanel"))


@app.route("/login", methods=["POST"])
def login():
    """Log a user in."""
    email, password = request.form["email"], request.form["password"]
    if not email_exists(email):
        return "Erreur : email invalide"
    if not check_password(email, password):
        return "Erreur : mot de passe invalide"
    session["email"] = email
    return redirect(url_for("testSelectionPanel"))


@app.route("/logout")
def logout():
    """Log the user out."""
    session.pop("email", None)
    return redirect(url_for("index"))


@app.route("/")
@login_required
def index():
    """Redirect to the test selection panel."""
    return redirect(url_for("testSelectionPanel"))


@app.route("/testSelectionPanel")
@login_required
def testSelectionPanel():
    """Show the menu of tests."""
    return render_template("testSelectionPanel.html")


@app.route("/congruentTest")
@login_required
def congruentTest():
    """Start a congruent-arrows session (testId 1)."""
    session["congruentTestSessionId"] = next_session_id(Result, session["email"], testId=1)
    return render_template("congruentTest.html")


@app.route("/nonCongruentTest")
@login_required
def nonCongruentTest():
    """Start a non-congruent-arrows session (testId 2)."""
    session["nonCongruentTestSessionId"] = next_session_id(Result, session["email"], testId=2)
    return render_template("nonCongruentTest.html")


@app.route("/results", methods=["POST"])
@login_required
def results():
    """Store all trials of an arrow test sent by static/script.js."""
    data = request.get_json()
    test_id = data["runningTest"]
    session_key = {1: "congruentTestSessionId", 2: "nonCongruentTestSessionId"}[test_id]
    for reaction_time, time_code, correct in zip(data["reactionTimes"], data["timeCodes"], data["isCorrect"]):
        db.session.add(Result(email=session["email"], sessionId=session[session_key], reactionTime=reaction_time,
                              timeCode=time_code, testId=test_id, isCorrect=correct, date=today()))
    db.session.commit()
    return jsonify(SAVED)


@app.route("/leaderboard")
@login_required
def leaderboard():
    """Show mean reaction time and accuracy per user, session and test."""
    rows = (
        db.session.query(Result.email, Result.sessionId, Result.testId,
                         func.avg(Result.reactionTime).label("average_reaction_time"),
                         (func.avg(Result.isCorrect) * 100).label("accuracy"))
        .group_by(Result.email, Result.sessionId, Result.testId)
        .order_by(func.avg(Result.reactionTime).filter(Result.isCorrect == 1))
        .all()
    )
    return render_template("leaderboard.html", results=rows)


@app.route("/ballTest")
@login_required
def ballTest():
    """Show the ball-tracking game."""
    return render_template("ballTest.html")


@app.route("/sendBallResult", methods=["POST"])
@login_required
def sendBallResult():
    """Store the score of the ball-tracking game."""
    email = session["email"]
    save(BallResult(email=email, sessionId=next_session_id(BallResult, email), score=request.get_json()["score"]))
    return jsonify(SAVED)


@app.route("/memoryPrisha")
@login_required
def memoryPrisha():
    """Show the image-recall and word-sequence memory games."""
    return render_template("memoryPrisha.html")


@app.route("/Prisha/images/<path:filename>")
@login_required
def serve_image(filename):
    """Serve the images of the image-recall game."""
    return send_from_directory("images", filename)


@app.route("/sendScorePrisha1", methods=["POST"])
@login_required
def sendScorePrisha1():
    """Store the score of the image-recall game."""
    email = session["email"]
    save(ResultPrisha1(email=email, sessionId=next_session_id(ResultPrisha1, email),
                       score=request.get_json()["score"], date=today()))
    return jsonify(SAVED)


@app.route("/sendScorePrisha2", methods=["POST"])
@login_required
def sendScorePrisha2():
    """Store the score of the word-sequence game."""
    email, data = session["email"], request.get_json()
    save(ResultPrisha2(email=email, sessionId=next_session_id(ResultPrisha2, email),
                       score=data["score"], nbMots=data["nbMots"], date=today()))
    return jsonify(SAVED)


@app.route("/memoryManon")
@login_required
def memoryManon():
    """Serve the number-sequence memory game (React build in Manon/)."""
    return send_from_directory("Manon", "index.html")


@app.route("/memoryManon/Manon/<path:path>")
@login_required
def serve_manon_build(path):
    """Serve the static files of the React build."""
    return send_from_directory("Manon", path)


if __name__ == "__main__":
    app.run(debug=True)
