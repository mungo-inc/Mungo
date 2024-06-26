import unittest
from app.index import Aliment 

class TestAliment(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()


    def test_eq(self) -> None:
        a1 = Aliment(0, "Patate", 0)
        a2 = Aliment(0, "Patate", 0)
        self.assertEqual(a1, a2)


    def test_eq2(self) -> None:
        a1 = Aliment(0, "Patate", 0)
        a2 = Aliment(1, "Sauce tomate", 0)
        self.assertNotEqual(a1, a2)


    def test_str(self) -> None:
        a1 = Aliment(0, "Patate", 0)
        self.assertEqual(str(a1), '\n\t(id: 0, nom: Patate, epicerie: 0)\n')
