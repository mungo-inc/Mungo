import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app.aliment import Aliment


class TestAliment(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()


    def test_eq(self) -> None:
        a1 = Aliment(0, "Patate", 0)
        a2 = Aliment(0, "Patate", 0)
        self.assertEqual(a1, a2)
        print("test_eq_aliment OK")


    def test_eq2(self) -> None:
        a1 = Aliment(0, "Patate", 0)
        a2 = Aliment(1, "Sauce tomate", 0)
        self.assertNotEqual(a1, a2)
        print("test_eq2_aliment OK")


    def test_str(self) -> None:
        a1 = Aliment(0, "Patate", 0)
        self.assertEqual(str(a1), '\n\t(id: 0, nom: Patate, epicerie: None)\n')
        print("test_str_aliment OK")
