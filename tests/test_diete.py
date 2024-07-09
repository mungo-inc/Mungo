import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app.diete import Diete


class TestAliment(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()


    def test_eq(self) -> None:
        d1 = Diete(0, "Omnivore")
        d2 = Diete(0, "Omnivore")
        self.assertEqual(d1, d2)
        print("test_eq_diete OK")


    def test_eq2(self) -> None:
        d1 = Diete(0, "Omnivoe")
        d2 = Diete(1, "Végétarienne")
        self.assertNotEqual(d1, d2)
        print("test_eq2_diete OK")


    def test_str(self) -> None:
        d1 = Diete(0, "Omnivore")
        self.assertEqual(str(d1), '\n\t(id: 0, nom: Omnivore)\n')
        print("test_str_diete OK")
