from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, Email, Result

app = Flask(__name__)
app.secret_key = 'aiot'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emails.db'
db.init_app(app)

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('attention'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    if verify_email(email):
        session['email'] = email
        return redirect(url_for('attention'))
    else:
        return 'Erreur : email invalide'

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    if not verify_email(email):
        register_email(email)
        session['email'] = email
        return redirect(url_for('attention'))
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
    email = data["email"]
    results = data["results"]

    result = Result(email=email, results=results)
    db.session.add(result)
    db.session.commit()

    return jsonify({"message": "Les résultats ont été enregistrés avec succès."})


def verify_email(email):
    return Email.query.filter_by(email=email).first() is not None

def register_email(email):
    email = Email(email=email)
    db.session.add(email)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
