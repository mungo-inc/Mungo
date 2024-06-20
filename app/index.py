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
    # diete = int(dietes[0])
    resultats = db.avoir_recettes(dietes, epiceries)
    # print(resultats)
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
            SELECT recette.Nom
            FROM recette
            JOIN recette_diete rd ON recette.id_Recette = rd.id_recette
            JOIN diete d ON rd.id_diète = d.id_diète
            WHERE rd.id_diète = {diete};
            """
        )
        curseur.execute(query)
        donnees = curseur.fetchall()
        return donnees


    def avoir_recettes(self, dietes, epiceries):
        donnees = []
        # if dietes == []:
        #     dietes = [0, 1, 2, 3, 4, 5, 6]
        for diete in dietes:
            donnees += self.filtrer_par_diete(diete)
        self.filtrer_par_epicerie(epiceries)
        #print(donnees)
        recettes_set = set(donnees)
        recettes = [construire_recette(donnee) for donnee in recettes_set]
        recettes.sort(key=lambda r : r['nom'])
        return recettes


    def filtrer_par_epicerie(self, epiceries):
        # On veut trouver les recettes dont tous les aliments sont disponibles
        # dans au moins une (on parle d'un OU) des épiceries se trouvant 
        # dans la liste `epiceries`
        curseur = self.get_connection().cursor()
        query = ( 
            """
            SELECT DISTINCT aliment_recette.id_recette, 
                            aliment_recette.id_aliment, 
                            aliment_epicerie.id_epicerie,
                            recette.nom as r_nom,
                            aliment.nom as a_nom
            FROM aliment_epicerie 
            JOIN aliment_recette ON aliment_epicerie.id_aliment = aliment_recette.id_aliment
            JOIN recette ON aliment_recette.id_recette = recette.id_recette
            JOIN aliment ON aliment_recette.id_aliment = aliment.id_aliment
            ORDER BY aliment_recette.id_recette
            """
        )
        curseur.execute(query)
        donnees = curseur.fetchall()
    
        recettes = {}
        recettes_epicerie = {}
    
        for (recette_id, aliment_id, epicerie_id, r_nom, a_nom) in donnees:
            aliment = Aliment(aliment_id, a_nom, epicerie_id)
            if recette_id not in recettes:
                recettes[recette_id] = Recette(recette_id, r_nom)
            recettes[recette_id].ajouter_aliment(aliment)
            
            if str(epicerie_id) in epiceries:
                if recette_id not in recettes_epicerie:
                    recettes_epicerie[recette_id] = Recette(recette_id, r_nom)
                recettes_epicerie[recette_id].ajouter_aliment(aliment)
    
        print(recettes)
        print("---")
        print(recettes_epicerie)
    
        resultat = []
        for recette_id, recette in recettes.items():
            if recette_id in recettes_epicerie:
                recette_epicerie = recettes_epicerie[recette_id]
                if recette.ont_memes_aliments(recette_epicerie):
                    resultat.append(recette)
        
        print("2---")
        print(resultat)
        return resultat


class Aliment():
    def __init__(self, id, nom, epicerie_id) -> None:
        self.id = id
        self.nom = nom
        self.epicerie_id = epicerie_id

    
    def __eq__(self, other):
        if isinstance(other, Aliment):
            return self.id == other.id
        return False


    def __str__(self):
        return f'\n\t(id: {self.id}, nom: {self.nom}, epicerie: {self.epicerie_id})\n'
    

    def __repr__(self) -> str:
        return str(self)


    def __hash__(self):
        return hash(self.id)


class Recette():
    def __init__(self, id, nom) -> None:
        self.id = id
        self.nom = nom
        self.aliments = set() 


    def __eq__(self, other):
        if isinstance(other, Recette):
            return self.id == other.id
        return False


    def __str__(self):
        return f'id: {self.id}, nom: {self.nom}, aliments: {self.aliments}\n'


    def __repr__(self) -> str:
        return str(self) 


    def ajouter_aliment(self, aliment: Aliment):
        self.aliments.add(aliment)


    def ont_memes_aliments(self, other):
        return (self.aliments == other.aliments)
