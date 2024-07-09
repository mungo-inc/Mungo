import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from app.index import app, db, Database, Client

class TestFormValidation(unittest.TestCase):
    def setUp(self) -> None:
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        pass

    #def tearDown(self):
    #    db.session.remove()
    #    db.drop_all()

    def test_validation_enregistrement(self):
        response = self.app.post('/register', data=dict(
                                courriel='test@example.com',
                                password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        client = Client.query.filter_by(courriel='test@example.com').first()
        self.assertIsNotNone(client)
        print("test_validation_enregistrement OK")

    def test_validation_enregistrement_false(self):
        response = self.app.post('/register', data=dict(
                                courriel='test2@example.com',
                                password=''
        ), follow_redirects=True)
        #self.assertEqual(response.status_code, 400)
        client = Client.query.filter_by(courriel='test2@example.com').first()
        self.assertIsNone(client)
        print("test_validation_enregistrement_false OK")



