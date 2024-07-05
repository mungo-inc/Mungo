import os
import re
from flask import Flask, render_template, g, redirect, request, session, url_for
from flask_login import LoginManager, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from .database import Database
import hashlib
import sqlite3

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = 'tv75JvcA3y' 
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'app', 'db', 'epicerie.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///../app/db/epicerie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from .client import Client

@login_manager.user_loader
def load_user(id_client):
    return Client.query.get(id_client)

@app.route('/', methods=['GET', 'POST'])
def accueil():
    if request.method == 'POST':
        session.pop('user', None)

        if request.form['password'] == 'password':
            session['user'] =  request.form['courriel']
            return render_template('index.html')
    return render_template('index.html')

@app.route('/panier')
def panier():
    return render_template('panier.html')

@app.route('/profil')
def profil():
    return render_template('profil.html')

@app.route('/compagnie')
def compagnie():
    return render_template('compagnie.html')

@app.route('/recettes')
def recettes():
    db = Database('app/db/epicerie.db')
    recettes = db.get_recettes()
    # return render_template('recettes.html', recettes=recettes)
    print(recettes)
    return render_template('resultats.html', resultats=recettes)


@app.route('/recette/<identifiant>')
def page_recette(identifiant):
    """
    retourne la page d'une recette selon son identifiant
    """
    db = Database('app/db/epicerie.db')
    print(identifiant)
    recette = db.get_recette(identifiant)
    aliments = []
    aliments = db.get_aliments_par_recette(identifiant)
    return render_template('recette.html', recette=recette, aliments=aliments)

@app.route('/articles')
def articles():
    db = Database('app/db/epicerie.db')
    articles = db.get_articles()
    return render_template('articles.html', articles=articles)

@app.route('/search', methods=['GET'])
def search():
    db = Database('app/db/epicerie.db')
    db.get_connection()
    # requete POST au lieu de GET?
    # aller chercher les valeurs cochées et le budget
    # avec ces valeurs, effectuer une query sql afin d'obtenir des resultats
    epiceries = request.args.getlist('epicerie')
    allergies = request.args.getlist('allergie')
    dietes = request.args.getlist('diete')
    budget = request.args['budget']
    resultats = db.avoir_recettes(allergies, dietes, epiceries)
    print("Donnee")
    print(resultats)
    return render_template('resultats.html', resultats=resultats)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        courriel = request.form['courriel']
        mot_passe = request.form['password'] 
        mot_passe_crypte = hashlib.sha256(mot_passe.encode()).hexdigest()
        user = Client.query.filter_by(courriel=courriel).first()
        
        if user and user.password == mot_passe_crypte:
            login_user(user)
            return redirect('/')

    return  redirect("/")


@app.route('/register', methods=['GET' , 'POST'])
def register():
    if request.method  ==  'GET':
        return render_template('index.html')
    elif request.method ==  'POST':

        courriel = request.form['courriel']
        mot_passe = request.form['password'] 
        mot_passe_crypte = hashlib.sha256(mot_passe.encode()).hexdigest()

        client = Client(courriel = courriel, password = mot_passe_crypte)

        db.session.add(client)
        db.session.commit()

    return redirect('/')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

def construire_recette(donnees):
    recettes = {}
    recettes["nom"] = donnees[0]
    return recettes

class Allergie():
    def __init__(self, id, nom) -> None:
        pass


