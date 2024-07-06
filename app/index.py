import os
import re
from flask import Flask, render_template
from flask import g, redirect, request, session, url_for
from flask_login import LoginManager, login_required
from flask_login import login_user, logout_user, user_logged_in, current_user
from flask import flash
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
    return Client.query.get(int(id_client))


@app.route('/', methods=['GET', 'POST'])
def accueil():
    liste_allergie = []
    liste_diete = [0]
    liste_epicerie = [0, 1, 2]
    if request.method == 'POST':
        session.pop('user', None)
        if request.form['password'] == 'password':
            session['user'] = request.form['courriel']
            return render_template('index.html')

    if current_user.is_authenticated:
        db = Database('app/db/epicerie.db')
        liste_allergie = db.construire_tableau_allergie(current_user.get_id())
        liste_diete = db.construire_tableau_diete(current_user.get_id())
        liste_epicerie = db.construire_tableau_epicerie(current_user.get_id())
        # (current_user.get_id())
    return render_template('index.html',
                           liste_allergie=liste_allergie,
                           liste_diete=liste_diete,
                           liste_epicerie=liste_epicerie)


@app.route('/panier')
def panier():
    return render_template('panier.html')


@app.route('/profil')
def profil():
    liste_allergie = []
    liste_diete = [0]
    liste_epicerie = [0, 1, 2]

    if current_user.is_authenticated:
        db = Database('app/db/epicerie.db')
        liste_allergie = db.construire_tableau_allergie(current_user.get_id())
        liste_diete = db.construire_tableau_diete(current_user.get_id())
        liste_epicerie = db.construire_tableau_epicerie(current_user.get_id())

    return render_template('profil.html',
                           liste_allergie=liste_allergie,
                           liste_diete=liste_diete,
                           liste_epicerie=liste_epicerie)


@app.route('/compagnie')
def compagnie():
    return render_template('compagnie.html')


@app.route('/recettes')
def recettes():
    db = Database('app/db/epicerie.db')
    recettes = db.get_recettes()
    return render_template('resultats.html', resultats=recettes)


@app.route('/articles')
def articles():
    db = Database('app/db/epicerie.db')
    articles = db.get_articles()
    return render_template('articles.html', articles=articles)


@app.route('/profil-modification', methods=['GET', 'POST'])
def modifier_preference():
    db = Database('app/db/epicerie.db')
    db.get_connection()
    epiceries = request.args.getlist('epicerie')
    allergies = request.args.getlist('allergie')
    dietes = request.args.getlist('diete')
    courriel = current_user.get_courriel()
    db.creation_requete_diete(courriel, dietes)
    db.creation_requete_epicerie(courriel, epiceries)
    db.creation_requete_allergie(courriel, allergies)

    flash("Les préférences ont bien été modifié.")
    return redirect('/profil')


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
        if not validation_mot_de_passe() or not validation_adresse_courriel():
            redirect('/incorrect')
        else:
            client = Client(courriel=courriel, password=mot_passe_crypte)
            db.session.add(client)
            db.session.commit()
            db_dur = Database('app/db/epicerie.db')
            db_dur.get_connection()
            db_dur.creation_requete_diete(courriel, [0])
            db_dur.creation_requete_epicerie(courriel, [0, 1, 2])

    return redirect('/')

@app.route("/incorrect")
def incorrect():
    '''Fonction qui renvoie la page en cas de mauvaise soumission'''
    return render_template("incorrect.html"), 400

@app.errorhandler(404)
def not_found_404(e):
    '''Fonction qui renvoie une page erreur 404'''
    return render_template('404.html'), 404

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def construire_recette(donnees):
    recettes = {}
    recettes["nom"] = donnees[0]

    return recettes

def validation_adresse_courriel():
    '''Valide adresse courriel à partir d'un regex'''
    valeur = True
    adresse_courriel = request.form["courriel"]
    if re.search(r"^\w+@\w+.\w{2,}$", adresse_courriel) is None:
        valeur = False
    return valeur

def validation_mot_de_passe():
    '''Valide un mot de passe'''
    return request.form["password"] != ""

class Allergie():
    def __init__(self, id, nom) -> None:
        pass
