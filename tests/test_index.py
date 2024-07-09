import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from flask import request
from pytest_mock import MockFixture
from app.index import app
custom_db_path = '../app/db/epicerie_test.db'

@pytest.fixture
def client():
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client

def test_accueil(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response = client.get("/")
    assert response.status_code == 200
    assert b"Bienvenue sur notre formulaire de recherche personnalis" in response.data


def test_panier(client):
    response = client.get("/panier")
    assert response.status_code == 200
    assert b"" in response.data


def test_profil(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response = client.get("/profil")
    assert response.status_code == 200
    assert b"Bienvenue sur notre formulaire pour changer vos" in response.data


def test_compagnie(client):
    response = client.get("/compagnie")
    assert response.status_code == 200
    assert b"" in response.data

def test_recettes(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response = client.get("/recettes")
    assert response.status_code == 200
    assert b"" in response.data

def test_articles(client, monkeypatch):
        monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
        response = client.get("/articles")
        assert response.status_code == 200
        assert b"Articles" in response.data

def test_modifier_preference(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response = client.get("/profil-modification")
    assert response.status_code == 200

def test_search(client, monkeypatch):
    with patch('app.index.get_query_params', return_value=(['0', '1', '2'], [], ['0'], 500)):
        monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
        response = client.get("/search")
        assert response.status_code == 200
        assert b"" in response.data

def test_login(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response = client.get("/login")
    assert response.status_code == 200
    assert b"" in response.data

def test_login_credentials(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response  = client.post("/login", data={
                            "courriel": "admin@1gmail.com",
                            "password": "admin",
    })
    assert response.status_code == 302

def test_register(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response = client.get("/register")
    assert response.status_code == 200
    assert b"" in response.data

def test_register_post(client, monkeypatch):
    monkeypatch.setitem(app.config, 'DATABASE_PATH', custom_db_path)
    response  = client.post("/register", data={
                            "courriel": "admin@1gmail.com",
                            "password": "admin",
    })
    assert response.status_code == 302

def test_incorrect(client):
    response = client.get("/incorrect")
    assert response.status_code == 400
    assert b"" in response.data

def test_logout_not_login(client):
    response = client.get("/logout")
    assert response.status_code == 401
    assert b"" in response.data

