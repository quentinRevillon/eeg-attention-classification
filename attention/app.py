from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, Email, Result
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'aiot'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attention.db'
db.init_app(app)


print(app.config['SQLALCHEMY_DATABASE_URI'])

app.app_context().push()     
db.create_all()
# with app.app_context():
#    db.create_all()


# from app import app, db
# app.app_context().push()
# db.drop_all()

# exit()

@app.route('/')
def index():
    session.clear()
    if 'email' in session:
        return redirect(url_for('testSelectionPanel.html'))
    return render_template('login.html')


@app.route('/testSelectionPanel')
def testSelectionPanel():
    if 'email' in session:
        return render_template('testSelectionPanel.html')
    return render_template('login.html')

@app.route('/congruentTest')
def congruentTest():
    if 'email' in session:
        return render_template('congruentTest.html')
    return render_template('login.html')

@app.route('/nonCongruentTest')
def nonCongruentTest():
    if 'email' in session:
        return render_template('nonCongruenttest.html')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    if verify_email(email):
        session['email'] = email
        return redirect(url_for('testSelectionPanel'))
    else:
        return 'Erreur : email invalide'

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    
    if not verify_email(email):
        print("je suis entré")
        register_email(email)
        session['email'] = email
        return redirect(url_for('testSelectionPanel.html'))
    else:
        return 'Erreur : email déjà utilisé'

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/attention')
def attention():
    if 'email' not in session:
        return redirect(url_for('index'))
    return render_template('attention.html')

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

        db.session.add(Result(id=id, email= email, session=session_id, reactionTime=reactionTimes[i], timeCode=timeCodes[i]))
        id += 1
        db.session.commit()

    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})


@app.route('/result', methods=['POST'])
def result():
    data = request.get_json()
    email = session['email']
    reactionTimes = data["reactionTime"]
    timeCodes = data["timeCode"]
    
    
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

        db.session.add(Result(id=id, email= email, session=session_id, reactionTime=reactionTimes[i], timeCode=timeCodes[i]))
        id += 1
        db.session.commit()

    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})


def verify_email(email):
    print("________________________________________________________________________________________________________________")
    return Email.query.filter_by(email=email).first() is not None


def register_email(email):
    email = Email(email=email)
    db.session.add(email)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
