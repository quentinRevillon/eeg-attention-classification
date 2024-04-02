from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Email {self.email}>'

class Result(db.Model):
    email = db.Column(db.String(120), db.ForeignKey('email.email'), nullable=False, primary_key=True)
    result1 = db.Column(db.Integer, nullable=False)
    result2 = db.Column(db.Integer, nullable=False)
    result3 = db.Column(db.Integer, nullable=False)
    result4 = db.Column(db.Integer, nullable=False)
    result5 = db.Column(db.Integer, nullable=False)
