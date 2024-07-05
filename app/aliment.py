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
        Redéfinition de l’opérateur “==” qui vérifie
        les IDs des aliments comme comparaison.
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
        Cette fonction permet d’utiliser l’ID de
        l’objet Aliment pour la fonction de hachage.
        """
        return hash(self.id)
