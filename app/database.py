import sqlite3
from .recette import Recette
from .aliment import Aliment
from .diete import Diete
from .panier import Panier
import math

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
        """
        Cette fonction permet de filtrer la recherche avec les allergies
        sélectionnées.
        Les allergies sélectionnées ne seront pas contenues dans le résultat.
        La fonction retourne une liste d’objets Recette.
        """
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
            recettes_allergies.append(Recette(nom, id_recette, None))
        return recettes_allergies

    def get_articles(self):
        """
        Cette fonction permet de prendre tous
        les aliments dans la base de données.
        """
        cursor = self.get_connection().cursor()
        query = 'SELECT * FROM Aliment'
        cursor.execute(query)
        articles = cursor.fetchall()
        return articles

    def get_recettes(self):
        """
        Cette fonction permet de prendre toutes
        les recettes dans la base de données.
        """
        cursor = self.get_connection().cursor()
        query = 'SELECT * FROM Recette'
        cursor.execute(query)
        resultat = cursor.fetchall()
        recettes = []
        for elem in resultat:
            id_recette = elem[0]
            nom = elem[1]
            recettes.append(Recette(id_recette, nom, None))
        resultat = self.get_aliments_par_recettes(recettes)
        resultat = self.get_recette_prix(recettes)
        return resultat 

    def get_recette(self, id_recette):
        """
            Cette fonction prend une recette dans la base de donnees
        """
        cursor = self.get_connection().cursor()
        query = f"""
                SELECT DISTINCT *
                FROM recette
                WHERE recette.id_recette = {id_recette}
        """
        cursor.execute(query)
        resultat = cursor.fetchone()
        recette = Recette(resultat[0], resultat[1], None) #None: temporaire
        return recette

    def get_aliments_par_recettes(self, recettes):
        resultat = []
        cursor = self.get_connection().cursor()
        query = """
                SELECT aliment.id_aliment, aliment.nom,
                aliment.Quantite, aliment_epicerie.id_epicerie, 
                aliment.Prix, aliment_recette.quantite, aliment.type
                FROM aliment
                JOIN aliment_recette ON aliment.id_aliment
                = aliment_recette.id_aliment
                JOIN aliment_epicerie ON aliment.id_aliment
                = aliment_epicerie.id_aliment
                WHERE aliment_recette.id_recette = ?
                """
        for recette in recettes:
            cursor.execute(query, (recette.id, ))
            aliments = cursor.fetchall()
            for (id, nom, quantite_aliment, epicerie, 
                 prix, quantite_recette, type_unite)  in aliments:
                aliment = Aliment(id, 
                                  nom, 
                                  quantite_aliment, 
                                  epicerie, 
                                  prix, 
                                  quantite_recette, 
                                  type_unite)
                recette.ajouter_aliment(aliment)
            resultat.append(recette)
        return resultat

    def get_aliments_par_recette(self, id_recette):
        cursor = self.get_connection().cursor()
        query = f"""
                SELECT DISTINCT aliment.id_aliment, aliment.nom, aliment_epicerie.id_epicerie
                FROM aliment 
                JOIN aliment_recette ON aliment.id_aliment = aliment_recette.id_aliment 
                JOIN aliment_epicerie ON aliment.id_aliment = aliment_epicerie.id_aliment 
                WHERE aliment_recette.id_recette = {id_recette}
                """
        cursor.execute(query)
        resultat = cursor.fetchall()
        aliments = []
        for id, nom, epicerie in resultat:
            aliment = Aliment(id, nom, epicerie)
            aliments.append(aliment)
        return set(aliments)

    def avoir_recettes(self, allergies, dietes, epiceries, budget):
        """
        Cette fonction permet de faire la recherche
        selon toutes les options sélectionnées de l’utilisateur.
        """
        donnees = []
        donnees_allergie = []
        donnees_diete = []
        donnees_epicerie = []
        donnees_allergie = set(self.filtrer_par_allergie(allergies))
        donnees_diete = set(self.filtrer_par_diete(dietes))
        donnees_epicerie = set(self.filtrer_par_epicerie(epiceries))
        donnees = donnees_epicerie & donnees_allergie & donnees_diete
        donnees_budget = set(self.filtrer_par_budget(donnees, budget))
        donnees = donnees_epicerie & donnees_allergie & donnees_diete & donnees_budget
        return self.get_aliments_par_recettes(sorted(donnees))  

    def filtrer_par_budget(self, donnees, budget):
        budget = int(budget)
        cursor = self.get_connection().cursor()
        query = """
            SELECT
                Aliment.ID_aliment,
                Aliment_Recette.ID_recette,
                Aliment_Recette.Quantite AS Quantite_Recette,
                Aliment.Quantite AS Quantite_Aliment,
                Aliment.Prix,
                Aliment.Type
            FROM
                Aliment
            JOIN
                Aliment_Recette ON Aliment.ID_aliment = Aliment_Recette.ID_aliment
            WHERE
                Aliment_Recette.ID_recette = ?;
        """
        nouvelle_donnees = []
        for recette in donnees:
            prix_total = 0  
            cursor.execute(query, (recette.id,))
            result = cursor.fetchall()
            ingredients_calculer = set()
            for row in result:
                aliment_id = row[0]
                quantite_recette = row[2]
                quantite_aliment = row[3]
                prix = row[4]
                Type = row[5]
                if aliment_id not in ingredients_calculer:
                    if quantite_aliment != 0 and (Type == 'u' or Type == 'l' or Type == 'g'):  
                        quantite = math.ceil(quantite_recette / quantite_aliment)
                        prix_total += quantite * prix
                        ingredients_calculer.add(aliment_id)
                    elif Type == 'p':
                        quantite = (quantite_recette / quantite_aliment)
                        prix_total += quantite * prix
                        ingredients_calculer.add(aliment_id)
            if prix_total <= budget:
                recette.prix =round(prix_total, 2 )
                nouvelle_donnees.append(recette)
        return nouvelle_donnees

    def get_recette_prix(self, donnees):
        cursor = self.get_connection().cursor()
        query = """
            SELECT
                Aliment.ID_aliment,
                Aliment_Recette.ID_recette,
                Aliment_Recette.Quantite AS Quantite_Recette,
                Aliment.Quantite AS Quantite_Aliment,
                Aliment.Prix,
                Aliment.Type
            FROM
                Aliment
            JOIN
                Aliment_Recette ON Aliment.ID_aliment = Aliment_Recette.ID_aliment
             WHERE
                Aliment_Recette.ID_recette = ?;

        """
        nouvelle_donnees = []
        for recette in donnees:
            prix_total = 0
            cursor.execute(query, (recette.id,))
            result = cursor.fetchall()
            ingredients_calculer = set()
            for row in result:
                aliment_id = row[0]
                quantite_recette = row[2]
                quantite_aliment = row[3]
                prix = row[4]
                Type = row[5]
                if aliment_id not in ingredients_calculer:
                    if quantite_aliment != 0 and (Type == 'u' or Type == 'l' or Type == 'g'):
                        quantite = math.ceil(quantite_recette / quantite_aliment)
                        prix_total += quantite * prix
                        ingredients_calculer.add(aliment_id)
                    elif Type == 'p':
                        quantite = (quantite_recette / quantite_aliment)
                        prix_total += quantite * prix
                        ingredients_calculer.add(aliment_id)
            recette.prix = round(prix_total,2)
            nouvelle_donnees.append(recette)
        return nouvelle_donnees






    def filtrer_par_diete(self, dietes):
        """
        Cette fonction permet de filtrer la recherche
        avec les diètes sélectionnées.
        La fonction retourne une liste d’objets Recette.
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
            if id_recette not in recettes:
                recettes[id_recette] = Recette(id_recette, r_nom, None)
            recettes[id_recette].ajouter_diete(diete)

            if str(id_diete) in dietes:
                if id_recette not in recettes_dietes:
                    recettes_dietes[id_recette] = Recette(id_recette, r_nom, None)
                recettes_dietes[id_recette].ajouter_diete(diete)

        resultat = []

        for id_recette, recette in recettes.items():
            if id_recette in recettes_dietes:
                resultat.append(recette)

        return resultat

    def filtrer_par_epicerie(self, epiceries):
        """
        Cette fonction permet de filtrer la recherche
        avec les épiceries sélectionnées.
        La fonction retourne une liste d’objets Recette.
        """
        curseur = self.get_connection().cursor()
        query = (
            """
            SELECT DISTINCT aliment_recette.id_recette,
                            aliment_recette.id_aliment,
                            aliment_epicerie.id_epicerie,
                            aliment_recette.quantite,
                            recette.nom as r_nom,
                            aliment.nom as a_nom
            FROM aliment_epicerie
            JOIN aliment_recette ON aliment_epicerie.id_aliment
            = aliment_recette.id_aliment
            JOIN recette ON aliment_recette.id_recette = recette.id_recette
            JOIN aliment ON aliment_recette.id_aliment = aliment.id_aliment
            ORDER BY aliment_recette.id_recette
            """
        )
        curseur.execute(query)
        donnees = curseur.fetchall()

        recettes = {}
        recettes_epicerie = {}

        for (recette_id, aliment_id, epicerie_id, quantite, r_nom, a_nom) in donnees:
            aliment = Aliment(aliment_id, a_nom, quantite, epicerie_id)
            if recette_id not in recettes:
                recettes[recette_id] = Recette(recette_id, r_nom, None)
            recettes[recette_id].ajouter_aliment(aliment)

            if str(epicerie_id) in epiceries:
                if recette_id not in recettes_epicerie:
                    recettes_epicerie[recette_id] = Recette(recette_id, r_nom, None)
                recettes_epicerie[recette_id].ajouter_aliment(aliment)

        resultat = []
        for recette_id, recette in recettes.items():
            if recette_id in recettes_epicerie:
                recette_epicerie = recettes_epicerie[recette_id]
                if recette.ont_memes_aliments(recette_epicerie):
                    resultat.append(recette)

        return resultat

    def construire_tableau_epicerie(self, id):
        query = (
            """
            SELECT id_epicerie
            FROM Client_Epicerie
            WHERE id_client = ?
            """
        )
        curseur = self.get_connection().cursor()
        curseur.execute(query, (id,))
        donnees = curseur.fetchall()

        resultat = []

        for id_epicerie in donnees:
            resultat.append(id_epicerie[0])

        return resultat

    def construire_tableau_diete(self, id):
        query = (
            """
            SELECT id_diete
            FROM Client_Diete
            WHERE id_client = ?
            """
        )
        curseur = self.get_connection().cursor()
        curseur.execute(query, (id,))
        donnees = curseur.fetchall()

        resultat = []

        for id_diete in donnees:
            resultat.append(id_diete[0])

        return resultat

    def construire_tableau_allergie(self, id):
        query = (
            """
            SELECT id_allergie
            FROM Client_Allergie
            WHERE id_client = ?
            """
        )
        curseur = self.get_connection().cursor()
        curseur.execute(query, (id,))
        donnees = curseur.fetchall()

        resultat = []

        for id_allergie in donnees:
            resultat.append(id_allergie[0])

        return resultat

    def creation_requete_diete(self, courriel, t_diete):
        query = (
            """
                SELECT id_client
                FROM    Client
                WHERE   courriel = ?
            """
        )
        curseur = self.get_connection().cursor()
        curseur.execute(query, (courriel, ))
        donnees = curseur.fetchone()

        query = (
            """
                SELECT  id_diete
                FROM    Client_Diete
                WHERE   id_client = ?
            """
        )
        curseur.execute(query, (donnees[0],))
        donnees_diete = curseur.fetchall()
        resultat_diete = []

        for id_diete in donnees_diete:
            resultat_diete.append(id_diete[0])
        set_diete = set(t_diete)
        set_db = set(resultat_diete)
        ensemble_diff = list(set_db - set_diete)

        for id_diete in ensemble_diff:
            query = (
                """
                    DELETE
                    FROM Client_Diete
                    WHERE id_client = ? AND id_diete = ?
                """
            )
            curseur.execute(query, (donnees[0], id_diete))
            self.get_connection().commit()

        for id_diete in t_diete:
            if id_diete not in resultat_diete:

                query = (
                    """
                        INSERT INTO Client_Diete VALUES (?, ?)
                    """
                )
            curseur.execute(query, (donnees[0], id_diete))
            self.get_connection().commit()

    def creation_requete_allergie(self, courriel, t_allergie):
        query = (
            """
                SELECT id_client
                FROM    Client
                WHERE   courriel = ?
            """
        )
        curseur = self.get_connection().cursor()
        curseur.execute(query, (courriel, ))
        donnees = curseur.fetchone()

        query = (
            """
                SELECT  id_allergie
                FROM    Client_Allergie
                WHERE   id_client = ?
            """
        )
        curseur.execute(query, (donnees[0],))
        donnees_allergie = curseur.fetchall()
        resultat_allergie = []

        for id_allergie in donnees_allergie:
            resultat_allergie.append(id_allergie[0])

        set_allergie = set(t_allergie)
        set_db = set(resultat_allergie)
        ensemble_diff = list(set_db - set_allergie)

        for id_allergie in ensemble_diff:
            query = (
                """
                    DELETE
                    FROM Client_Allergie
                    WHERE id_client = ? AND id_allergie = ?
                """
            )
            curseur.execute(query, (donnees[0], id_allergie))
            self.get_connection().commit()

        for id_allergie in t_allergie:
            if id_allergie not in resultat_allergie:

                query = (
                    """
                        INSERT INTO Client_Allergie VALUES (?, ?)
                    """
                )
            curseur.execute(query, (donnees[0], id_allergie))
            self.get_connection().commit()

    def creation_requete_epicerie(self, courriel, t_epicerie):
        query = (
            """
                SELECT id_client
                FROM    Client
                WHERE   courriel = ?
            """
        )
        curseur = self.get_connection().cursor()
        curseur.execute(query, (courriel, ))
        donnees = curseur.fetchone()

        query = (
            """
                SELECT  id_epicerie
                FROM    Client_Epicerie
                WHERE   id_client = ?
            """
        )
        curseur.execute(query, (donnees[0],))
        donnees_epicerie = curseur.fetchall()
        resultat_epicerie = []

        for id_epicerie in donnees_epicerie:
            resultat_epicerie.append(str(id_epicerie[0]))

        set_epicerie = set(t_epicerie)
        set_db = set(resultat_epicerie)
        ensemble_diff = list(set_db - set_epicerie)

        for id_epicerie in ensemble_diff:
            query = (
                 """
                    DELETE
                    FROM Client_Epicerie
                    WHERE id_client = ? AND id_epicerie = ?
                """
            )
            curseur.execute(query, (donnees[0], id_epicerie))
            self.get_connection().commit()

        for id_epicerie in t_epicerie:
            if id_epicerie not in resultat_epicerie:
                query = (
                    """
                        INSERT INTO Client_Epicerie VALUES (?, ?)
                    """
                )
                curseur.execute(query, (donnees[0], id_epicerie))
                self.get_connection().commit()

    def sauvegarder_panier(self, id_client, data):
        id_panier = self.generer_panier_id(id_client)
        nom_panier = self.generer_nom_panier(id_client)
        for recette in data:
            for aliment in recette['aliments']:
                query = (
                    """
                    INSERT INTO Client_Panier_Aliment_Recette 
                    VALUES (?, ?, ?, ?, ?)
                    """
                )
                curseur.execute(query, 
                    (
                        id_panier, 
                        id_client, 
                        aliment['id'], 
                        recette['id'], 
                        nom_panier
                    )
                )
                self.get_connection().commit()
    

    def generer_nom_panier(self, id_client):
        nombre_paniers = self.get_nombre_paniers(id_client)
        return f"Liste d'épicerie #{int(nombre_paniers) + 1}"

    def generer_panier_id(self, id_client):
        curseur = self.get_connection().cursor()
        query = (
            """
            SELECT id_panier
            FROM Client_Panier_Aliment_Recette
            WHERE id_client = (?)
            ORDER BY id_panier DESC
            LIMIT 1
            """
        )
        curseur.execute(query, (id_client, ))
        id = curseur.fetchone()
        if id is None:
            return 0
        print(f"generated ID: {id}")
        return int(id[0]) + 1

    def get_paniers(self, id_client):
        curseur = self.get_connection().cursor()
        query = (
            """
            SELECT *
            FROM Client_Panier_Aliment_Recette
            WHERE id_client = (?)
            """
        )
        curseur.execute(query, (id_client, ))
        items = curseur.fetchall()
        paniers = []
        for item in items:
            panier, recette, aliment = None, None, None
            panier = Panier(item[0], item[1], [], item[4])
            if panier not in paniers:
                paniers.append(panier)
            recette = Recette(item[3], self.get_nom_recette(item[3]), None) # None: temporaire
            if recette not in paniers[-1].recettes:
                paniers[-1].ajouter_recette(recette)
            aliment = Aliment(item[2], self.get_nom_aliment(item[2]))
            paniers[-1].recettes[-1].ajouter_aliment(aliment)
        return paniers

    def get_nombre_paniers(self, id_client):
        curseur = self.get_connection().cursor()
        query = (
            """
            SELECT COUNT(DISTINCT id_panier)
            FROM Client_Panier_Aliment_Recette
            WHERE id_client = (?)
            """
        )
        curseur.execute(query, (id_client, ))
        result = curseur.fetchone()
        if result is not None:
            return result[0]
        return 0 


    def get_nom_aliment(self, id_aliment):
        """
        Permet d'obtenir le nom d'un aliment selon un ID
        """
        curseur = self.get_connection().cursor()
        query = (
            """
            SELECT aliment.nom
            FROM aliment
            WHERE id_aliment = (?)
            """
        )
        curseur.execute(query, (id_aliment, ))
        nom = curseur.fetchone()
        return nom[0]

    def get_nom_recette(self, id_recette):
        """
        Permet d'obtenir le nom d'une recette selon un ID
        """
        curseur = self.get_connection().cursor()
        query = (
            """
            SELECT recette.nom
            FROM recette 
            WHERE id_recette = (?)
            """
        )
        curseur.execute(query, (id_recette, ))
        nom = curseur.fetchone()
        return nom[0]


    def supprimer_panier(self, id_client):
        pass
