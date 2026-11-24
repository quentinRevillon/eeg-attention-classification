"""SQLAlchemy models of the web app database (users and game results).

Usage:
    from models import db, User, Result
    db.init_app(app)
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Participant account; ``password`` is a pbkdf2 hash."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Result(db.Model):
    """One arrow trial of the attention tests (testId 1 = congruent, 2 = non-congruent).

    ``reactionTime`` and ``timeCode`` are in ms; ``timeCode`` counts from the start of the test
    and is used to align the trial with the EEG recording.
    """

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey("user.email"), nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    reactionTime = db.Column(db.Integer, nullable=False)
    timeCode = db.Column(db.Integer, nullable=False)
    testId = db.Column(db.Integer, nullable=False)
    isCorrect = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(120), nullable=False)


class BallResult(db.Model):
    """Score of the ball-tracking game."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey("user.email"), nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)


class ResultPrisha1(db.Model):
    """Score of the image-recall memory game."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey("user.email"), nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(120), nullable=False)


class ResultPrisha2(db.Model):
    """Score of the word-sequence memory game, with the sequence length ``nbMots``."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey("user.email"), nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    nbMots = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(120), nullable=False)
