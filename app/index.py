import re
from flask import Flask 
from flask import render_template 
from flask import g 
from flask import redirect 
from flask import request
from .database import Database
#from diete import Diete
#from aliment import Aliment
#from recette import Recette
#import sqlite3

app = Flask(__name__, static_url_path="", static_folder="static")

@app.route('/')
def accueil():
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


def construire_recette(donnees):
    recettes = {}
    recettes["nom"] = donnees[0]

    return recettes
  
class Allergie():
    def __init__(self, id, nom) -> None:
        pass
