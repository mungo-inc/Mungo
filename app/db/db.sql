CREATE TABLE Aliment (
    ID_aliment INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL,
    Type TEXT NOT NULL,
    Quantite REAL NULL,
    Prix REAL NOT NULL,
    Vedette Boolean
);

CREATE TABLE Recette (
    ID_recette INTEGER PRIMARY KEY AUTOINCREMENT,
    Nom TEXT NOT NULL,
    Moyenne_note REAL
);

CREATE TABLE Aliment_Recette (
    ID_aliment INTEGER,
    ID_recette INTEGER,
    Quantite   REAL,
    PRIMARY KEY (ID_aliment, ID_recette),
    FOREIGN KEY (ID_aliment) REFERENCES Aliment(ID_aliment),
    FOREIGN KEY (ID_recette) REFERENCES Recette(ID_recette)
);

CREATE TABLE Avis (
    ID_avis INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_recette INTEGER NOT NULL,
    ID_client INTEGER,
    Nom TEXT NOT NULL,
    Note INTEGER NOT NULL,
    Opinion TEXT,
    Date DATE DEFAULT (DATE('now')),
    FOREIGN KEY (ID_recette) REFERENCES Recette(ID_recette),
    FOREIGN KEY (ID_client) REFERENCES Client(ID_client)
);

CREATE TABLE Client (
    ID_client INTEGER PRIMARY KEY AUTOINCREMENT,
    courriel TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE Panier (
    ID_panier INTEGER PRIMARY KEY,
    ID_client INTEGER,
    Prix REAL NOT NULL,
    FOREIGN KEY (ID_client) REFERENCES Client(ID_client)
);

CREATE TABLE Panier_Aliment (
    ID_panier INTEGER,
    ID_aliment INTEGER,
    Quantite_aliment INTEGER NOT NULL,
    PRIMARY KEY (ID_panier, ID_aliment),
    FOREIGN KEY (ID_panier) REFERENCES Panier(ID_panier),
    FOREIGN KEY (ID_aliment) REFERENCES Aliment(ID_aliment)
);

CREATE TABLE Allergie (
    ID_allergie INTEGER PRIMARY KEY,
    Type TEXT NOT NULL
);

CREATE TABLE Client_Allergie (
    ID_client INTEGER,
    ID_allergie INTEGER,
    PRIMARY KEY (ID_client, ID_allergie),
    FOREIGN KEY (ID_client) REFERENCES Client(ID_client),
    FOREIGN KEY (ID_allergie) REFERENCES Allergie(ID_allergie)
);

CREATE TABLE Diete (
    ID_diete INTEGER PRIMARY KEY,
    Type TEXT NOT NULL
);

CREATE TABLE Recette_diete (
    ID_recette INTEGER,
    ID_diete INTEGER,
    PRIMARY KEY (ID_recette, ID_diete),
    FOREIGN KEY (ID_recette) REFERENCES Recette(ID_recette),
    FOREIGN KEY (ID_diete) REFERENCES Diete(ID_diete)
);

CREATE TABLE Client_diete (
    ID_client INTEGER,
    ID_diete INTEGER,
    PRIMARY KEY (ID_client, ID_diete),
    FOREIGN KEY (ID_client) REFERENCES Client(ID_client),
    FOREIGN KEY (ID_diete) REFERENCES Diete(ID_diete)
);

CREATE TABLE Epicerie (
    ID_epicerie INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL 
);

CREATE TABLE Aliment_epicerie (
    ID_aliment INTEGER,
    ID_epicerie INTEGER,
    Prix REAL NOT NULL,
    PRIMARY KEY (ID_aliment, ID_epicerie)
);

CREATE TABLE Aliment_Allergie (
    ID_aliment INTEGER,
    ID_allergie INTEGER,
    PRIMARY KEY (ID_aliment, ID_allergie),
    FOREIGN KEY (ID_aliment) REFERENCES Aliment(ID_aliment),
    FOREIGN KEY (ID_allergie) REFERENCES Allergie(ID_allergie)
);

CREATE TABLE Client_Epicerie (
    ID_Client INTEGER,
    ID_Epicerie INTEGER,
    PRIMARY KEY (ID_client, ID_epicerie)
);

CREATE TABLE Client_Panier_Aliment_Recette (
    ID_panier INTEGER,
    ID_client INTEGER,
    ID_aliment INTEGER,
    ID_recette INTEGER,
    Nom TEXT,
    PRIMARY KEY (ID_panier, ID_client, ID_aliment, ID_recette),
    FOREIGN KEY (ID_panier) REFERENCES Panier(ID_panier),
    FOREIGN KEY (ID_aliment) REFERENCES Aliment(ID_aliment),
    FOREIGN KEY (ID_recette) REFERENCES Recette(ID_recette)
);

CREATE TABLE Client_Recette (
  ID_client INTEGER,
  ID_recette INTEGER,
  PRIMARY KEY (ID_client, ID_recette),
  FOREIGN KEY (ID_Client) REFERENCES Client(ID_client),
  FOREIGN KEY (ID_recette) REFERENCES Recette(ID_recette)
);
