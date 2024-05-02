from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attention.db'
db.init_app(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<Email {self.email} >'

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    reactionTime = db.Column(db.Integer, nullable=False)
    timeCode = db.Column(db.Integer, nullable=False)
    testId = db.Column(db.Integer, nullable=False)
    
class BallResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
class ResultPrisha1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    # gameId = db.Column(db.Integer, nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

class ResultPrisha2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    # gameId = db.Column(db.Integer, nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    nbMots = db.Column(db.Integer, nullable=False)

class ResultManon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), db.ForeignKey('user.email'), nullable=False)
    gameId = db.Column(db.Integer, nullable=False)
    sessionId = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    

with app.app_context():
    db.create_all()
    # result2 = db.Column(db.Integer, nullable=False)
    # result3 = db.Column(db.Integer, nullable=False)
    # result4 = db.Column(db.Integer, nullable=False)
    # result5 = db.Column(db.Integer, nullable=False)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     reactions = db.relationship('Reaction', backref='user', lazy=True)

# class Reaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     session_id = db.Column(db.Integer, nullable=False)
#     reaction_time = db.Column(db.Float, nullable=False)
    
