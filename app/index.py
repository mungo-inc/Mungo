import re
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
    db = Database('app/db/epicerie.db')
    recettes = db.get_recettes()
    return render_template('recettes.html', recettes=recettes)

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
    return render_template('resultats.html', resultats=resultats)


def construire_recette(donnees):
    recettes = {}
    recettes["nom"] = donnees[0]

    return recettes


class Database:
    def __init__(self, path):
        self.connection = None
        self.path = path

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.path)
        return self.connection

    def filtrer_par_allergie(self, allergie):
        curseur = self.get_connection().cursor()
        query = (
                f"""
                SELECT DISTINCT recette.nom
                FROM recette
                JOIN aliment_recette ar ON recette.id_recette = ar.id_recette
                JOIN aliment_allergie aa ON aa.id_aliment = ar.id_aliment
                JOIN allergie ON allergie.id_allergie = aa.id_allergie
                WHERE recette.id_recette NOT IN (
                    SELECT ar.id_recette
                    FROM aliment_recette ar
                    JOIN aliment_allergie aa ON aa.id_aliment = ar.id_aliment
                    JOIN allergie a ON a.id_allergie = aa.id_allergie
                    WHERE a.type IN ('Poisson')
                    );
                """
                )
        curseur.execute(query)
        donnees = curseur.fetchall()
        return donnees


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
    
    def get_articles(self):
        cursor = self.get_connection().cursor()
        query = 'SELECT * FROM Aliment'
        cursor.execute(query)
        articles = cursor.fetchall()
        return articles

    def get_recettes(self):
        cursor = self.get_connection().cursor()
        query = 'SELECT * FROM Recette'
        cursor.execute(query)
        recettes = cursor.fetchall()
        print(recettes)
        resultat = self.get_aliments_par_recettes(cursor, recettes)
        print(resultat)
        return recettes


    def get_aliments_par_recettes(self, cursor, recettes):
        resultat = []
        query = """
                SELECT aliment.nom 
                FROM aliment 
                JOIN aliment_recette ON aliment.id_aliment = aliment_recette.id_aliment 
                WHERE aliment_recette.id_recette = ?
                """
        for elem in recettes:
            id_recette = elem[0]
            cursor.execute(query, (id_recette,))
            aliments = cursor.fetchall()
            resultat.append(elem + (aliments, ))
        return resultat 


    def avoir_recettes(self, allergies, dietes, epiceries):
        donnees = []
        donnees_diete = []
        donnees_epicerie = []
       
        donnees_diete = set(self.filtrer_par_diete1(dietes))
        donnees_epicerie = set(self.filtrer_par_epicerie(epiceries))
        donnees = donnees_epicerie & donnees_diete
        return sorted(donnees)

    def filtrer_par_diete1(self, dietes):
        curseur = self.get_connection().cursor()
        query = (
            """
            SELECT DISTINCT recette_diete.id_recette,
                            recette_diete.id_diete,
                            recette.nom as r_nom,
                            diete.type as d_nom
            FROM recette_diete
            JOIN recette ON recette_diete.id_recette = recette.id_recette
            JOIN diete ON recette_diete.id_diete = diete.id_diete
            ORDER BY recette_diete.id_recette
            """
        )
        curseur.execute(query)
        donnees = curseur.fetchall()

        recettes = {}
        recettes_dietes = {}

        for (id_recette, id_diete, r_nom, d_nom) in donnees:
            diete = Diete(id_diete, d_nom)
            if  id_recette not in recettes:
                recettes[id_recette] = Recette(id_recette, r_nom)
            recettes[id_recette].ajouter_diete(diete)

            if str(id_diete) in dietes:
                if id_recette not in recettes_dietes:
                    recettes_dietes[id_recette] = Recette(id_recette, r_nom)
                recettes_dietes[id_recette].ajouter_diete(diete)

        resultat = []

        for id_recette, recette in recettes.items():
            if  id_recette in recettes_dietes:
                resultat.append(recette)

        return resultat

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
    
        resultat = []
        for recette_id, recette in recettes.items():
            if recette_id in recettes_epicerie:
                recette_epicerie = recettes_epicerie[recette_id]
                if recette.ont_memes_aliments(recette_epicerie):
                    resultat.append(recette)
        
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

class Diete():

    def __init__(self, id, nom) -> None:
        self.id = id
        self.nom = nom

    def __eq__(self, other):
        if isinstance(other, Diete):
            return self.id == other.id
        return False

    def __str__(self):
        return f'id: {self.id}, nom: {self.nom}'

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash(self.id)

class Recette():
    def __init__(self, id, nom) -> None:
        self.id = id
        self.nom = nom
        self.aliments = set()
        self.dietes = set()


    def __eq__(self, other):
        if isinstance(other, Recette):
            return self.id == other.id
        return False


    def __str__(self):
        return f'id: {self.id}, nom: {self.nom}, aliments: {self.aliments}, diete: {self.dietes}\n'


    def __repr__(self) -> str:
        return str(self) 

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.nom < other.nom

    def ajouter_aliment(self, aliment: Aliment):
        self.aliments.add(aliment)

    def ajouter_diete(self, diete: Diete):
        self.dietes.add(diete)

    def ont_memes_aliments(self, other):
        return (self.aliments == other.aliments)

class Allergie():
    def __init__(self, id, nom) -> None:
        pass
