class Panier:
    def __init__(self, id, id_client, recettes=[], nom=None) -> None:
        self.id = id
        self.id_client = id_client
        self.recettes = recettes
        self.nom = nom
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Panier):
            return self.id == other.id
        return False
    
    def __hash__(self):
        return hash(self.id)

    def ajouter_recette(self, recette):
        self.recettes.append(recette)

    def __str__(self) -> str:
        return f"id: {self.id}, {self.recettes}"
        
    def __repr__(self) -> str:
        """
        Retourne des paniers selon le string definie pour un tableau.
        """
        return str(self)
