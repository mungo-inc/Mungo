CREATE TABLE Aliment (
    Id_aliment INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL,
    Prix REAL NOT NULL,
    Type TEXT NOT NULL,
    Epicerie TEXT NOT NULL
);

CREATE TABLE Recette (
    Id_Recette INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL,
    Moyenne_note REAL
);

CREATE TABLE Aliment_Recette (
    Id_aliment INTEGER,
    Id_Recette INTEGER,
    PRIMARY KEY (Id_aliment, Id_Recette),
    FOREIGN KEY (Id_aliment) REFERENCES Aliment(Id_aliment),
    FOREIGN KEY (Id_Recette) REFERENCES Recette(Id_Recette)
);

CREATE TABLE Critique (
    Id_Recette INTEGER,
    Id_critique INTEGER PRIMARY KEY,
    Note INTEGER NOT NULL,
    Commentaires TEXT,
    FOREIGN KEY (Id_Recette) REFERENCES Recette(Id_Recette)
);

CREATE TABLE Client (
    Id_Client INTEGER PRIMARY KEY,
    Nom TEXT NOT NULL,
    Mot_de_passe TEXT NOT NULL
);

CREATE TABLE Panier (
    Id_panier INTEGER PRIMARY KEY,
    Id_Client INTEGER,
    Prix REAL NOT NULL,
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client)
);

CREATE TABLE Panier_Aliment (
    Id_panier INTEGER,
    Quantité_aliment INTEGER NOT NULL,
    Id_aliment INTEGER,
    PRIMARY KEY (Id_panier, Id_aliment),
    FOREIGN KEY (Id_panier) REFERENCES Panier(Id_panier),
    FOREIGN KEY (Id_aliment) REFERENCES Aliment(Id_aliment)
);

CREATE TABLE Allergie (
    Id_Allergie INTEGER PRIMARY KEY,
    Type TEXT NOT NULL
);

CREATE TABLE Client_Allergie (
    Id_Client INTEGER,
    Id_Allergie INTEGER,
    PRIMARY KEY (Id_Client, Id_Allergie),
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client),
    FOREIGN KEY (Id_Allergie) REFERENCES Allergie(Id_Allergie)
);

CREATE TABLE Diète (
    Id_diète INTEGER PRIMARY KEY,
    Type TEXT NOT NULL
);

CREATE TABLE Recette_diète (
    Id_recette INTEGER,
    Id_diète INTEGER,
    PRIMARY KEY (Id_recette, Id_diète),
    FOREIGN KEY (Id_recette) REFERENCES Recette(Id_Recette),
    FOREIGN KEY (Id_diète) REFERENCES Diète(Id_diète)
);

CREATE TABLE Recette_Allergie (
    Id_recette INTEGER,
    Id_Allergie INTEGER,
    PRIMARY KEY (Id_recette, Id_Allergie),
    FOREIGN KEY (Id_recette) REFERENCES Recette(Id_Recette),
    FOREIGN KEY (Id_Allergie) REFERENCES Allergie(Id_Allergie)
);

CREATE TABLE Client_diète (
    Id_Client INTEGER,
    Id_Diète INTEGER,
    PRIMARY KEY (Id_Client, Id_Diète),
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client),
    FOREIGN KEY (Id_Diète) REFERENCES Diète(Id_diète)
);
