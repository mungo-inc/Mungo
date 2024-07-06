class Diete():
    def __init__(self, id, nom) -> None:
        """
        Constructeur de l’objet Diete.
        """
        self.id = id
        self.nom = nom

    def __eq__(self, other):
        """
        Redéfinition de l’opérateur “==” qui vérifie
        les IDs des diètes comme comparaison.
        """
        if isinstance(other, Diete):
            return self.id == other.id
        return False

    def __str__(self):
        """
        Cette fonction permet d’afficher un objet diète en string.
        """
        return f'\n\t(id: {self.id}, nom: {self.nom})\n'

    def __repr__(self) -> str:
        """
        Retourne des aliments selon le string definie pour un tableau.
        """
        return str(self)

    def __hash__(self):
        """
        Cette fonction permet d’utiliser l’ID de
        l’objet Diete pour la fonction de hachage.
        """
        return hash(self.id)
