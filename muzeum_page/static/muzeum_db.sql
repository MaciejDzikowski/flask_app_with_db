-- DROP EXISTING TABLES

DROP TABLE IF EXISTS Eksponaty CASCADE;
DROP TABLE IF EXISTS Artysci CASCADE;
DROP TABLE IF EXISTS Galerie CASCADE;
DROP TABLE IF EXISTS Historia CASCADE;
DROP TABLE IF EXISTS Uzytkownicy CASCADE;


-- CREATE TABLES

CREATE TABLE IF NOT EXISTS Artysci (
    Nazwisko VARCHAR(100) NOT NULL,
    Rok_urodzenia integer NOT NULL,
    Rok_smierci integer,
    PRIMARY KEY (Nazwisko)
);

CREATE TABLE IF NOT EXISTS Galerie (
    Nazwa VARCHAR(100) NOT NULL,
    Pojemnosc integer NOT NULL,
    PRIMARY KEY (Nazwa)
);

CREATE TABLE IF NOT EXISTS Eksponaty (
    Tytul VARCHAR(200) NOT NULL,
    Typ VARCHAR(100) NOT NULL,
    Wysokosc integer NOT NULL,
    Szerokosc integer NOT NULL,
    Artysta_Nazwisko VARCHAR(100),
    Galeria_Nazwa VARCHAR(100),
    PRIMARY KEY (Tytul),
    FOREIGN KEY (Artysta_Nazwisko) REFERENCES Artysci(Nazwisko),
    FOREIGN KEY (Galeria_Nazwa) REFERENCES Galerie(Nazwa)
);

CREATE TABLE IF NOT EXISTS Historia (
    ID SERIAL NOT NULL,
    Eksponat_Tytul VARCHAR(200) NOT NULL,
    Galeria_Nazwa VARCHAR(100) NOT NULL,
    Poczatek DATE NOT NULL,
    Koniec DATE,
    PRIMARY KEY (ID),
    FOREIGN KEY (Eksponat_Tytul) REFERENCES Eksponaty(Tytul),
    FOREIGN KEY (Galeria_Nazwa) REFERENCES Galerie(Nazwa)
);

CREATE TABLE IF NOT EXISTS Uzytkownicy (
    ID integer NOT NULL,
    Nazwa VARCHAR(50) NOT NULL,
    Haslo VARCHAR NOT NULL,  -- NOT A PROPER WAY OF STORING PASSWORD
    PRIMARY KEY (ID)
);


-- INSERT VALUES

INSERT INTO Artysci (Nazwisko, Rok_urodzenia, Rok_smierci) VALUES ('Leo Helo', 1459, 1510);

INSERT INTO Galerie (Nazwa, Pojemnosc) VALUES('Mala', 5);
INSERT INTO Galerie (Nazwa, Pojemnosc) VALUES('Duza', 7);

INSERT INTO Eksponaty (Tytul, Typ, Wysokosc, Szerokosc, Artysta_Nazwisko, Galeria_Nazwa) VALUES ('Monia', 'obraz', 60, 50, 'Leo Helo', 'Mala');
INSERT INTO Eksponaty (Tytul, Typ, Wysokosc, Szerokosc, Artysta_Nazwisko, Galeria_Nazwa) VALUES ('Wenus', 'rzezba', 10, 5, NULL, NULL);

INSERT INTO Historia (Eksponat_Tytul, Galeria_Nazwa, Poczatek, Koniec) VALUES ('Monia', 'Duza', '1980-05-12', '1985-05-12');
INSERT INTO Historia (Eksponat_Tytul, Galeria_Nazwa, Poczatek, Koniec) VALUES ('Monia', 'Mala', '1996-05-12', NULL);
INSERT INTO Historia (Eksponat_Tytul, Galeria_Nazwa, Poczatek, Koniec) VALUES ('Wenus', 'Mala', '2002-05-12', '2004-05-12');

INSERT INTO Uzytkownicy (ID, Nazwa, Haslo) VALUES (1, 'User', crypt('1234', get_salt('salt')));
