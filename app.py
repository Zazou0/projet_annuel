# Importation des modules nécessaires de Flask
from flask import Flask, request, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Création d'une nouvelle application Flask
app = Flask(__name__)

# Configuration de l'application pour utiliser une base de données SQLite locale
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'votre_clé_secrète_générée_aléatoirement'

# Initialisation de l'objet SQLAlchemy
db = SQLAlchemy(app)

# Définition du modèle User pour la table 'user'
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

# Définition du modèle Car pour la table 'car'
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_plate = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Création de toutes les tables de la base de données (si elles n'existent pas déjà)
with app.app_context():
    db.create_all()

@app.route('/create_test_user', methods=['GET'])
def create_test_user():
    # Création d'un nouvel utilisateur
    new_user = User(username='test', password='test')
    db.session.add(new_user)
    db.session.commit()
    
    return "Test user created successfully"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            return "User not found"
        elif user.password != password:
            return "Incorrect password"
        else:
            session['username'] = username
            return redirect(url_for('account'))  # Redirige l'utilisateur vers la fonction qui gère la route /account
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return "User logged out successfully"

@app.route('/account')
def account():
    username = session.get('username')
    
    if username is None:
        return redirect(url_for('login'))
        
    else:
        return render_template('account.html', username=username)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')





# Si ce module est le fichier principal exécuté, exécutez l'application
if __name__ == "__main__":
    app.run(debug=True)
