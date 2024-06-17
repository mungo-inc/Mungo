from flask import Flask 
from flask import render_template 
from flask import g 
from flask import redirect 
from flask import request
import sqlite3

app = Flask(__name__, static_url_path="", static_folder="static")

@app.route('/')
def accueil():
    return render_template('index.html')


@app.route('/recettes')
def recettes():
    return render_template('recettes.html')


@app.route('/search', methods=['GET'])
def search():
    db = Database()
    db.get_connection()
    # requete POST au lieu de GET?
    # aller chercher les valeurs cochées et le budget
    # avec ces valeurs, effectuer une query sql afin d'obtenir des resultats
    epiceries = request.args.getlist('epicerie')
    allergies = request.args.getlist('allergie')
    dietes = request.args.getlist('diete')
    budget = request.args['budget']
    diete = int(dietes[0])
    resultats = db.avoir_recettes(dietes)
    print(resultats)
    return render_template('resultats.html', resultats=resultats)

def construire_recette(donnees):
    recettes = {}
    recettes["nom"] = donnees[0]

    return recettes

class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('app/db/epicerie.db')
        return self.connection


    def filtrer_par_diete(self, diete):
        curseur = self.get_connection().cursor()
        query = (
            f"""
            SELECT r.Nom
            FROM Recette r
            JOIN Recette_diete rd ON r.Id_Recette = rd.Id_recette
            JOIN Diete d ON rd.Id_diète = d.Id_diète
            WHERE rd.id_diète = {diete};
            """
        )
        curseur.execute(query)
        donnees = curseur.fetchall()
        return donnees


    def avoir_recettes(self, dietes):
        donnees = []
        for diete in dietes:
            donnees += self.filtrer_par_diete(diete)
        print(donnees)
        recettes_set = set(donnees)
        recettes = [construire_recette(donnee) for donnee in recettes_set]
        recettes.sort(key=lambda r : r['nom'])
        return recettes
