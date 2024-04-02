from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')


    # Importez les modules nécessaires pour la connexion à la base de données

    # Créez une fonction pour vérifier les informations de connexion dans la base de données
def verify_credentials(email, password):
    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécutez une requête pour vérifier les informations de connexion
    query = "SELECT * FROM users WHERE email= AND password=?"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()

    # Fermez la connexion à la base de données
    cursor.close()
    conn.close()

    # Vérifiez si les informations de connexion sont valides
    if result:
        return True
    else:
        return False



# Utilisez la fonction verify_credentials dans la route login pour vérifier les informations de connexion
@app.route('/connexion', methods=['POST'])
def login():
    email = request.form['email']
    

    # Vérifiez les informations de connexion en utilisant la fonction verify_credentials
    if verify_credentials(email, password):
        # Authentification réussie, rediriger vers une page de succès
        return redirect(url_for('success'))
    else:
        # Authentification échouée, afficher un message d'erreur sur la page de connexion
        error_message = "Adresse e-mail ou mot de passe incorrect"
        return render_template('login.html', error_message=error_message)

@app.route('/connexion', methods=['POST'])
def login():
    

    
    email = request.form['email']
    password = request.form['password']

    print(email, password)
    
    # Ajoutez ici votre logique de vérification des informations de connexion
    
    # Exemple simple de vérification (remplacez par votre propre logique)
    if email == 'example@example.com' and password == 'password':
        # Authentification réussie, rediriger vers une page de succès
        return redirect(url_for('success'))
    else:
        # Authentification échouée, afficher un message d'erreur sur la page de connexion
        error_message = "Adresse e-mail ou mot de passe incorrect"
        return render_template('login.html', error_message="login failed")

@app.route('/success')
def success():
    return "Connexion réussie !"

if __name__ == '__main__':
    app.run(debug=True)
