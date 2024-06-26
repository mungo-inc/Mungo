import unittest
from app.index import Recette
from app.index import Aliment 

class TestRecette(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_eq1(self) -> None:
        r1 = Recette(1, "Pizza")
        r2 = Recette(1, "")
        self.assertEqual(r1, r2)


    def test_eq2(self) -> None:
        r1 = Recette(1, "Pizza")
        r2 = Recette(2, "")
        self.assertNotEqual(r1, r2)


    def test_str(self) -> None:
        r1 = Recette(1, "Pizza")
        self.assertEqual(str(r1), 'id: 1, nom: Pizza, aliments: set()\n')


    def test_ajouter_aliment(self) -> None:
        r2 = Recette(1, "Spaghetti")
        a1 = Aliment(0, "Patate", 0)
        a2 = Aliment(1, "Pomme", 0)
        r2.ajouter_aliment(a1)
        r2.ajouter_aliment(a2)
        self.assertEqual(r2.aliments, set([a1, a2]))


    def test_ont_memes_aliment1(self) -> None:
        r2 = Recette(1, "Spaghetti")
        a1 = Aliment(0, "Patate", 0)
        a2 = Aliment(1, "Pomme", 0)
        r2.ajouter_aliment(a1)
        r2.ajouter_aliment(a2)
        self.assertTrue(r2.ont_memes_aliments(r2))
    

    def test_ont_memes_aliment2(self) -> None:
        r2 = Recette(1, "Spaghetti")
        r1 = Recette(1, "Spaghetti")
        a1 = Aliment(0, "Patate", 0)
        a2 = Aliment(1, "Pomme", 0)
        r2.ajouter_aliment(a1)
        r2.ajouter_aliment(a2)
        r1.ajouter_aliment(a2)
        self.assertFalse(r1.ont_memes_aliments(r2))
