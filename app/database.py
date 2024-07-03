import sqlite3
from .recette import Recette
from .aliment import Aliment
from .diete import Diete


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
            recettes_allergies.append(Recette(nom, id_recette))
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
            recettes.append(Recette(id_recette, nom))
        resultat = self.get_aliments_par_recettes(recettes)
        return resultat

    def get_aliments_par_recettes(self, recettes):
        resultat = []
        cursor = self.get_connection().cursor()
        query = """
                SELECT aliment.id_aliment, aliment.nom,
                aliment_epicerie.id_epicerie
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
            for id, nom, epicerie in aliments:
                aliment = Aliment(id, nom, epicerie)
                recette.ajouter_aliment(aliment)
            resultat.append(recette)
        return resultat

    def avoir_recettes(self, allergies, dietes, epiceries):
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
        return self.get_aliments_par_recettes(sorted(donnees))

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
                recettes[id_recette] = Recette(id_recette, r_nom)
            recettes[id_recette].ajouter_diete(diete)

            if str(id_diete) in dietes:
                if id_recette not in recettes_dietes:
                    recettes_dietes[id_recette] = Recette(id_recette, r_nom)
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
