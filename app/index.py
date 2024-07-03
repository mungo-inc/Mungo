import os
import re
from flask import Flask, render_template
from flask import g, redirect, request, session, url_for
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, user_logged_in, current_user
from flask_sqlalchemy import SQLAlchemy
from .database import Database
import hashlib
import sqlite3

client_id = None
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
    return Client.query.get(int(id_client))


@app.route('/', methods=['GET', 'POST'])
def accueil():
    liste_allergie = []
    liste_diete = [0]
    # liste_epicerie = []
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['password'] == 'password':
            session['user'] = request.form['courriel']
            return render_template('index.html')

    if current_user.is_authenticated:
        db = Database('app/db/epicerie.db')
        liste_allergie = db.construire_tableau_allergie(current_user.get_id())
        liste_diete = db.construire_tableau_diete(current_user.get_id())
        # liste_epicerie = db.construire_tableau_epicerie
        # (current_user.get_id())
    return render_template('index.html',
                           liste_allergie=liste_allergie,
                           liste_diete=liste_diete)


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

    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        courriel = request.form['courriel']
        mot_passe = request.form['password']
        mot_passe_crypte = hashlib.sha256(mot_passe.encode()).hexdigest()

        client = Client(courriel=courriel, password=mot_passe_crypte)

        db.session.add(client)
        db.session.commit()
        db_dur = Database('app/db/epicerie.db')
        db_dur.get_connection()
        db_dur.creation_requete_diete(courriel, 0)

    return redirect('/')


@app.route('/logout')
@login_required
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
