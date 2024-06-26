from .aliment import Aliment
from .diete import Diete

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
