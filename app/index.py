import os
import re
from flask import Flask, render_template, jsonify
from flask import g, redirect, request, session, url_for
from flask_login import LoginManager, login_required, UserMixin
from flask_login import login_user, logout_user, user_logged_in, current_user
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from .database import Database
import hashlib
import imghdr
import sqlite3

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = 'tv75JvcA3y'
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'app', 'db', 'epicerie.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///../app/db/epicerie.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DATABASE_PATH'] = 'app/db/epicerie.db'
UPLOAD_FOLDER = 'app/static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

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
    db = Database(app.config['DATABASE_PATH'])
    paniers = db.get_paniers(current_user.get_id())
    return render_template('panier.html', paniers=paniers)


@app.route('/profil')
def profil():
    liste_allergie = []
    liste_diete = [0]
    liste_epicerie = [0, 1, 2]

    if current_user.is_authenticated:
        db = Database(app.config['DATABASE_PATH'])
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

@app.route('/ajout-recette')
@login_required
def ajouter_recette():
    db = Database(app.config['DATABASE_PATH'])
    ingredients = db.get_articles()
    return render_template('ajout-recette.html', ingredients=ingredients)

@app.route('/get_ingredients')
def get_ingredients():
    db = Database(app.config['DATABASE_PATH'])
    ingredients = db.get_articles()
    return jsonify(ingredients)

@app.route('/recettes')
def recettes():
    db = Database(app.config['DATABASE_PATH'])
    recettes = db.get_recettes()

    return render_template('resultats.html', resultats=recettes)


@app.route('/recette/<identifiant>')
def page_recette(identifiant):
    """
    retourne la page d'une recette selon son identifiant
    """
    db = Database('app/db/epicerie.db')
    recette = db.get_recette(identifiant)
    aliments = db.get_aliments_par_recette(identifiant)
    avis = db.get_avis_par_recette(identifiant)
    return render_template('recette.html', recette=recette, aliments=aliments, avis=avis)

@app.route('/articles')
def articles():
    db = Database(app.config['DATABASE_PATH'])
    articles = db.get_articles()
    return render_template('articles.html', articles=articles)


@app.route('/profil-modification', methods=['GET', 'POST'])
def modifier_preference():
    db = Database(app.config['DATABASE_PATH'])
    db.get_connection()
    epiceries = request.args.getlist('epicerie')
    allergies = request.args.getlist('allergie')
    dietes = request.args.getlist('diete')
    courriel = current_user.get_courriel()
    db.creation_requete_diete(courriel, dietes)
    db.creation_requete_epicerie(courriel, epiceries)
    db.creation_requete_allergie(courriel, allergies)

    flash("Les préférences ont bien été modifiées.")
    return redirect('/profil')


@app.route('/envoyer-recette', methods=['GET', 'POST'])
def envoyer_recette():
    db = Database(app.config['DATABASE_PATH'])
    dernier_id_recette = db.chercher_dernier_id_recette()
    if validation_partager_recette() and upload_file(dernier_id_recette): 
        nom = request.form["nom-recette"]
        ingredients = request.form.getlist("ingredients")
        ingredients_quantite = []
        for ingredient in ingredients:
            quantite = request.form[ingredient+"-quantite"]
            ingredients_quantite.append([ingredient,quantite])
        dietes = request.form.getlist('diete')
        id = current_user.get_id()
        db.ajouter_recette_db(id, nom, ingredients_quantite, dietes)
        return redirect('/ajout-recette')
    else: 
        return redirect('/incorrect')
def est_chiffre(chiffre):
    try:
        float(chiffre)
        return True
    except ValueError:
        return False

def validation_partager_recette():
    nom = request.form["nom-recette"]
    ingredients = request.form.getlist("ingredients")
    ingredients_quantite = []
    if  nom == "":
        return False
    elif len(ingredients) == 0:
        return False
    for ingredient in ingredients:
        quantite = request.form[ingredient+"-quantite"]
        ingredients_quantite.append([ingredient,quantite])
        if not est_chiffre(ingredient) or not est_chiffre(quantite):
            return False
    dietes = request.form.getlist('diete')
    if len(dietes) == 0:
        return False
    return True

def upload_file(dernier_id_recette):
    if 'image-recette' not in request.files:
        print('Pas de fichier')
        return True

    file = request.files['image-recette']

    if file.filename == '':
        return True

    if file:
        file_content = file.read()
        file_type = imghdr.what(None, file_content)
        print(file_type)
        file.seek(0)

        if file_type != 'jpeg':
            print('Le fichier n\'est pas un fichier JPG')
            return False

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])


        filename = str(dernier_id_recette) + ".jpg"
        if isinstance(filename, str) and filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            return True
        else:
            return False

    return False

def get_query_params():
    epiceries = request.args.getlist('epicerie')
    allergies = request.args.getlist('allergie')
    dietes = request.args.getlist('diete')
    budget = request.args.get('budget') 
    return epiceries, allergies, dietes, budget

@app.route('/produit_vedette')
def produit_vedette():
    db = Database(app.config['DATABASE_PATH'])
    articles = db.get_articles()
    return render_template('/produit_vedette.html', articles=articles)

@app.route('/faire_produit_vedette', methods=["POST"])
def faire_produit_vedette():
    db = Database(app.config['DATABASE_PATH'])
    id_vedette = request.form["dropdown"]
    db.ajouter_vedette(id_vedette)
    print(id_vedette)
    return redirect("/")

@app.route('/search', methods=['GET'])
def search():
    db = Database(app.config['DATABASE_PATH'])
    db.get_connection()
    epiceries, allergies, dietes, budget = get_query_params()
    resultats = db.avoir_recettes(allergies, dietes, epiceries, budget)
    for recette in resultats:
        print(f"Recette ID: {recette.id}, Prix: {recette.prix}, Contient Vedette: {recette.vedette}")
    
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
        utilisateur = Client.query.filter_by(courriel=courriel).first()
        if utilisateur:
            return redirect('/')

        if not validation_mot_de_passe() or not validation_adresse_courriel():
            redirect('/incorrect')
        else:
            client = Client(courriel=courriel, password=mot_passe_crypte)
            db_dur = Database(app.config['DATABASE_PATH'])
            db_dur.get_connection()
            query = (
            """
                insert into client (courriel, password) values (?, ?)
            """
            )
            curseur = db_dur.get_connection().cursor()
            curseur.execute(query, (client.courriel, client.password))
            db_dur.get_connection().commit() 
            db_dur.creation_requete_diete(courriel, [0])
            db_dur.creation_requete_epicerie(courriel, [0, 1, 2])
            user = Client.query.filter_by(courriel=courriel).first()

            if user and user.password == mot_passe_crypte:
                login_user(user)
                return redirect('/')


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



@app.route('/sauvegarder-liste', methods=['POST'])
def save_list():
    db = Database('app/db/epicerie.db')
    data = request.get_json()
    db.sauvegarder_panier(current_user.id_client, data)
    return jsonify({"message": "Liste sauvegardée avec succès."})


@app.route('/supprimer-liste', methods=['POST'])
def delete_list():
    db = Database('app/db/epicerie.db')
    data = request.get_json()
    db.supprimer_panier(data['idClient'], data['idPanier'])
    return jsonify({"message": "Liste supprimée avec succès."})


@app.route('/sauvegarder-modif-liste', methods=['POST'])
def save_modification_list():
    db = Database('app/db/epicerie.db')
    data = request.get_json()
    print(data)
    db.modifier_panier(data['idClient'], data['idPanier'], data['nouveauNom'])
    return jsonify({"message": "Liste modifiée avec succès."})

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

class Client(db.Model, UserMixin):
    __tablename__ = 'client'

    id_client = db.Column(db.Integer, primary_key=True)
    courriel = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text,  nullable=False)

    def __init__(self, courriel, password):
        self.courriel = courriel
        self.password = password

    def get_id(self):
        return str(self.id_client)

    def get_courriel(self):
        return str(self.courriel)


@app.route('/avis-recette', methods=['POST'])
def post_avis():
    if request.method == "POST":
        id_recette = request.form.get("id_recette")
        nom = request.form.get("nom")
        if nom is None or nom.strip() == "":
            nom = "Anonyme"
        note = request.form.get("note")
        if note is None or note.strip() == "":
            note = 0
        opinion = request.form.get("opinion")
        if current_user.is_authenticated:
            id_client = current_user.id_client
            nom = current_user.courriel
        else:
            id_client = 9999
        db = Database(app.config['DATABASE_PATH'])
        db.get_connection()
        db.sauvegarder_avis(id_recette, id_client, nom, note, opinion)
        return redirect(url_for('page_recette', identifiant=id_recette))

    return redirect(url_for('incorrect'))
