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
    print(resultats)
    return render_template('resultats.html', resultats=resultats)


def construire_recette(donnees):
    recettes = {}
    recettes["nom"] = donnees[0]

    return recettes


class Database:
    def __init__(self, path):
        """
        Constructeur pour la classe Database.
        """
        self.connection = None
        self.path = path

    def get_connection(self):
        """
        Cette fonction permet de se connecter à la base de données.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.path)
        return self.connection

    def filtrer_par_allergie(self, allergies):
        #Cette fonction permet de filtrer la recherche avec les allergies sélectionnées. Les allergies sélectionnées ne seront pas contenues dans le résultat. La fonction retourne une liste d’objets Recette.
        allergies = ', '.join(f"'{allergie}'" for allergie in allergies)
        curseur = self.get_connection().cursor()
        query = (
                f"""
                SELECT DISTINCT r.id_recette, r.nom 
                FROM recette r
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM aliment_recette ar
                    JOIN aliment_allergie aa ON ar.id_aliment = aa.id_aliment
                    JOIN allergie a ON aa.id_allergie = a.id_allergie
                    WHERE ar.id_recette = r.id_recette
                    AND a.id_allergie IN ({allergies})
                    );
	            """
                )
        curseur.execute(query)
        donnees = curseur.fetchall()
        recettes_allergies = []
        for (nom, id_recette) in donnees:
            recettes_allergies.append(Recette(nom, id_recette)) 
        return recettes_allergies
    
    def get_articles(self):
        """
        Cette fonction permet de prendre tous les aliments dans la base de données.
        """
        cursor = self.get_connection().cursor()
        query = 'SELECT * FROM Aliment'
        cursor.execute(query)
        articles = cursor.fetchall()
        return articles

    def get_recettes(self):
        """
        Cette fonction permet de prendre toutes les recettes dans la base de données.
        """
        cursor = self.get_connection().cursor()
        query = 'SELECT * FROM Recette'
        cursor.execute(query)
        recettes = cursor.fetchall()
        resultat = self.get_aliments_par_recettes(cursor, recettes)
        return resultat 


    def get_aliments_par_recettes(self, cursor, recettes):
        resultat = []
        query = """
                SELECT aliment.id_aliment, aliment.nom, aliment_epicerie.id_epicerie
                FROM aliment 
                JOIN aliment_recette ON aliment.id_aliment = aliment_recette.id_aliment 
                JOIN aliment_epicerie ON aliment.id_aliment = aliment_epicerie.id_aliment 
                WHERE aliment_recette.id_recette = ?
                """
        for elem in recettes:
            id_recette = elem[0]
            nom = elem[1]
            recette = Recette(id_recette, nom)
            cursor.execute(query, (id_recette, ))
            aliments = cursor.fetchall()
            for id, nom, epicerie in aliments:
                aliment = Aliment(id, nom, epicerie)
                recette.ajouter_aliment(aliment)
            resultat.append(recette)
        return resultat 

    def avoir_recettes(self, allergies, dietes, epiceries):
        """
        Cette fonction permet de faire la recherche selon toutes les options sélectionnées de l’utilisateur.
        """
        donnees = []
        donnees_allergie = []
        donnees_diete = []
        donnees_epicerie = []
        donnees_allergie = set(self.filtrer_par_allergie(allergies))
        print(donnees_allergie)
        donnees_diete = set(self.filtrer_par_diete(dietes))
        donnees_epicerie = set(self.filtrer_par_epicerie(epiceries))
        donnees = donnees_epicerie & donnees_allergie & donnees_diete
        return sorted(donnees)

    def filtrer_par_diete(self, dietes):
        """
        Cette fonction permet de filtrer la recherche avec les diètes sélectionnées. La fonction retourne une liste d’objets Recette.
        """
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
        """
        Cette fonction permet de filtrer la recherche avec les épiceries sélectionnées. La fonction retourne une liste d’objets Recette.
        """
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
        """
        Constructeur de l’objet Aliment.
        """
        self.id = id
        self.nom = nom
        self.epicerie_id = epicerie_id

    
    def __eq__(self, other):
        """
        Redéfinition de l’opérateur “==” qui vérifie les IDs des aliments comme comparaison.
        """
        if isinstance(other, Aliment):
            return self.id == other.id
        return False


    def __str__(self):
        """
        Cette fonction permet d’afficher un objet Aliment en string.
        """
        return f'\n\t(id: {self.id}, nom: {self.nom}, epicerie: {self.epicerie_id})\n'
    

    def __repr__(self) -> str:
        """
        Retourne des aliments selon le string definie pour un tableau.
        """
        return str(self)


    def __hash__(self):
        """
        Cette fonction permet d’utiliser l’ID de l’objet Aliment pour la fonction de hachage.
        """
        return hash(self.id)

class Diete():
    def __init__(self, id, nom) -> None:
        """
        Constructeur de l’objet Diete.
        """
        self.id = id
        self.nom = nom

    def __eq__(self, other):
        """
        Redéfinition de l’opérateur “==” qui vérifie les IDs des diètes comme comparaison.
        """
        if isinstance(other, Diete):
            return self.id == other.id
        return False

    def __str__(self):
        """
        Cette fonction permet d’afficher un objet diète en string.
        """
        return f'id: {self.id}, nom: {self.nom}'

    def __repr__(self) -> str:
        """
        Retourne des aliments selon le string definie pour un tableau.
        """
        return str(self)

    def __hash__(self):
        """
        Cette fonction permet d’utiliser l’ID de l’objet Diete pour la fonction de hachage.
        """
        return hash(self.id)

class Recette():
    def __init__(self, id, nom) -> None:
        """
        Constructeur de l’objet Recette.
        """
        self.id = id
        self.nom = nom
        self.aliments = set()
        self.dietes = set()


    def __eq__(self, other):
        """
        Redéfinition de l’opérateur “==” qui vérifie les IDs des recettes comme comparaison.
        """
        if isinstance(other, Recette):
            return self.id == other.id
        return False


    def __str__(self):
        """
        Cette fonction permet d’afficher un objet Recette en string.
        """
        return f'id: {self.id}, nom: {self.nom}, aliments: {self.aliments}, diete: {self.dietes}\n'


    def __repr__(self) -> str:
        """
        Retourne des aliments selon le string definie pour un tableau
        """
        return str(self)

    def __hash__(self):
        """
        Cette fonction permet d’utiliser l’ID de l’objet Recette pour la fonction de hachage.-
        """
        return hash(self.id)

    def __lt__(self, other):
        """
        Redéfinition de l’opérateur “<” qui vérifie les noms des recettes comme comparaison.
        """
        return self.nom < other.nom

    def ajouter_aliment(self, aliment: Aliment):
        """
        Cette fonction permet d’ajouter un aliment dans l’objet Recette.
        """
        self.aliments.add(aliment)

    def ajouter_diete(self, diete: Diete):
        """
        Cette fonction permet d’ajouter une diète dans l’objet Recette.
        """
        self.dietes.add(diete)

    def ont_memes_aliments(self, other):
        """
        Cette fonction vérifie si deux recettes ont le même aliment.
        """
        return (self.aliments == other.aliments)

class Allergie():
    def __init__(self, id, nom) -> None:
        pass
