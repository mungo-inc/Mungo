import unittest
from unittest import mock
from app.index import Database

class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database(":memory:")
        pass
