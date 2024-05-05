from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from models import db, User, Result, BallResult, ResultPrisha1, ResultPrisha2
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'aiot'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attention.db'
db.init_app(app)

def myLoginManager(funcToProtect):
    @wraps(funcToProtect)
    def funcProtected(*args, **kwargs):
        print("hello")
        if 'email' in session and emailMatchPassword(session['email'], session['password']):
            
            return funcToProtect(*args, **kwargs)
        return render_template('login.html')
    return funcProtected
def emailMatchPassword(email, password):
    # print(user.email)
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return True
    return False


def verify_email(email):
    print("________________________________________________________________________________________________________________")
    return User.query.filter_by(email=email).first() is not None


def register_user(email, hashed_password):
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()


print(app.config['SQLALCHEMY_DATABASE_URI'])

app.app_context().push()
db.create_all()
with app.app_context():
   db.create_all()


# from app import app, db
# app.app_context().push()
# db.drop_all()

# exit()
@app.route('/Prisha/images/<path:filename>')
@myLoginManager
def serve_image(filename):
    return send_from_directory('images', filename)

@app.route('/memoryManon')
@myLoginManager
def memoryManon():
    # if 'email' in session and emailMatchPassword(session['email'], session['password']):
    return send_from_directory('Manon', 'index.html')
    # return render_template('login.html')

@app.route('/memoryManon/Manon/static/css/<path:path>')
@myLoginManager
def serve_static_css(path):
    print(path)
    return send_from_directory('Manon/static/css/', path)

@app.route('/memoryManon/Manon/static/js/<path:path>')
@myLoginManager
def serve_static_js(path):
    print(path)
    return send_from_directory('Manon/static/js/', path)

@app.route('/memoryManon/Manon/manifest.json')
@myLoginManager
def serve_manifest():
    return send_from_directory('Manon/', 'manifest.json')

@app.route('/memoryPrisha')
@myLoginManager
def memoryPrisha():
    # if 'email' in session and emailMatchPassword(session['email'], session['password']):
    return render_template('memoryPrisha.html')
    # return render_template('login.html')

@app.route('/sendScorePrisha1', methods=['POST'])
@myLoginManager
def sendScorePrisha1():
    data = request.get_json()
    print(data)
    score=data["score"]
    email=session['email']
    # gameId=data["gameId"]
    sessionId = db.session.query(func.max(Result.sessionId)).filter(Result.email == email).scalar()
    sessionId = sessionId + 1 if sessionId is not None else 1
    db.session.add(ResultPrisha1(email=email, sessionId=sessionId, score=score))
    db.session.commit()
    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})

@app.route('/sendScorePrisha2', methods=['POST'])
@myLoginManager
def sendScorePrisha2():
    data = request.get_json()
    print(data)
    score=data["score"]
    email=session['email']
    nbMots=data["nbMots"]
    sessionId = db.session.query(func.max(Result.sessionId)).filter(Result.email == email).scalar()
    sessionId = sessionId + 1 if sessionId is not None else 1
    db.session.add(ResultPrisha2(email=email, sessionId=sessionId, score=score, nbMots=nbMots))
    db.session.commit()
    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})
    
@app.route('/sendScoreManon', methods=['POST'])
@myLoginManager
def sendScoreManon():
    data = request.get_json()
    print(data)
    score=data["score"]
    email=session['email']
    gameId=data["gameId"]
    sessionId = db.session.query(func.max(Result.sessionId)).filter(Result.email == email).scalar()
    sessionId = sessionId + 1 if sessionId is not None else 1
    db.session.add(ResultPrisha(email=email, gameId=gameId, sessionId=sessionId, score=score))
    db.session.commit()
    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})

@app.route('/sendBallResult', methods=['POST'])
@myLoginManager
def sendBallResult():
    data = request.get_json()
    print(data)
    score=data["score"]
    email=session['email']
    sessionId = db.session.query(func.max(Result.sessionId)).filter(Result.email == email).scalar()
    sessionId = sessionId + 1 if sessionId is not None else 1
    db.session.add(BallResult(email=email, sessionId=sessionId, score=score))
    db.session.commit()
    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})

@app.route('/')
@myLoginManager
def index():
    # session.clear()
    # if 'email' in session and emailMatchPassword(session['email'], session['password']):
    return redirect(url_for('testSelectionPanel'))
    # return render_template('login.html')


@app.route('/testSelectionPanel')
@myLoginManager
def testSelectionPanel():
    # if 'email' in session and emailMatchPassword(session['email'], session['password']):
    return render_template('testSelectionPanel.html')
    # return render_template('login.html')

@app.route('/congruentTest')
@myLoginManager
def congruentTest():
    # if 'email' in session and emailMatchPassword(session['email'], session['password']):
    email = session['email']
    session['congruentTestSessionId'] = db.session.query(func.max(Result.sessionId)).filter(Result.email == email).filter(Result.testId == 1).scalar()
    session['congruentTestSessionId'] = session['congruentTestSessionId'] + 1 if session['congruentTestSessionId'] is not None else 1
    return render_template('congruentTest.html')
    # return render_template('login.html')

@app.route('/nonCongruentTest')
@myLoginManager
def nonCongruentTest():
    # if 'email' in session and emailMatchPassword(session['email'], session['password']):
    email = session['email']
    session['nonCongruentTestSessionId'] = db.session.query(func.max(Result.sessionId)).filter(Result.email == email).filter(Result.testId == 2).scalar()
    session['nonCongruentTestSessionId'] = session['nonCongruentTestSessionId'] + 1 if session['nonCongruentTestSessionId'] is not None else 1
    return render_template('nonCongruentTest.html')
    # return render_template('login.html')

@app.route('/ballTest')
@myLoginManager
def ballTest():
    # if 'email' in session and emailMatchPassword(session['email'], session['password']):
        
    return render_template('ballTest.html')
        
    # return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    if verify_email(email):
        if emailMatchPassword(email, password):
            session['email'] = email
            session['password'] = password
            return redirect(url_for('testSelectionPanel'))
        else:
            return 'Erreur : mot de passe invalide'
    else:
        return 'Erreur : email invalide'

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']

    if not verify_email(email):
        print("je suis entré")
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        register_user(email, hashed_password)
        session['email'] = email
        session['password'] = password
     
        return redirect(url_for('testSelectionPanel'))
    else:
        return 'Erreur : email déjà utilisé'


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/results', methods=['POST'])
def results():
    data = request.get_json()
    email = session['email']
    reactionTimes = data["reactionTimes"]
    timeCodes = data["timeCodes"]

     # Récupérer l'ID maximal actuel de la colonne "session" dans la table "Result"
    session_id = db.session.query(func.max(Result.session)).scalar()

    # Si aucun ID maximal n'est trouvé, définir le nouvel ID de session à 1
    # Sinon, ajouter 1 à l'ID maximal actuel pour obtenir le nouvel ID de session
    session_id = session_id if session_id is not None else 0
    session_id += 1

    # Récupérer l'ID maximal actuel de la colonne "session" dans la table "Result"
    id = db.session.query(func.max(Result.id)).scalar()

    # Si aucun ID maximal n'est trouvé, définir le nouvel ID de session à 1
    # Sinon, ajouter 1 à l'ID maximal actuel pour obtenir le nouvel ID de session
    id = id if id is not None else 0
    id += 1

    for i in range(len(reactionTimes)):

        db.session.add(Result(id=id, email= email, sessionId=session_id, reactionTime=reactionTimes[i], timeCode=timeCodes[i]))
        id += 1
        db.session.commit()

    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})



@app.route('/result', methods=['POST'])
@myLoginManager
def result():
    data = request.get_json()
    email = session['email']
    reactionTime = data["reactionTime"]
    timeCode = data["timeCode"]
    runningTest = data["runningTest"]
    
    
     # Récupérer l'ID maximal actuel de la colonne "session" dans la table "Result"
    if runningTest == 1:
        sessionId = session['congruentTestSessionId']
    elif runningTest == 2:
        sessionId = session['nonCongruentTestSessionId']
    


    # # Récupérer l'ID maximal actuel de la colonne "session" dans la table "Result"
    # id = db.session.query(func.max(Result.id)).scalar()

    # # Si aucun ID maximal n'est trouvé, définir le nouvel ID de session à 1
    # # Sinon, ajouter 1 à l'ID maximal actuel pour obtenir le nouvel ID de session
    # id = id + 1 if id is not None else 1
    
    db.session.add(Result(email= email, sessionId=sessionId, reactionTime=reactionTime, timeCode=timeCode, testId=runningTest))
    db.session.commit()

    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})




if __name__ == '__main__':
    app.run(debug=True)
