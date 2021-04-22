from . import db
from flask_login import UserMixin


class Artysci(db.Model):
    nazwisko = db.Column(db.Text, primary_key=True)
    rok_urodzenia = db.Column(db.Integer, nullable=False)
    rok_smierci = db.Column(db.Integer)


class Galerie(db.Model):
    nazwa = db.Column(db.Text, primary_key=True)
    pojemnosc = db.Column(db.Integer, nullable=False)


class Eksponaty(db.Model):
    tytul = db.Column(db.Text, primary_key=True)
    typ = db.Column(db.Text, nullable=False)
    wysokosc = db.Column(db.Integer, nullable=False)
    szerokosc = db.Column(db.Integer, nullable=False)
    artysta_nazwisko = db.Column(db.Text, db.ForeignKey('artysci.nazwisko'))
    galeria_nazwa = db.Column(db.Text, db.ForeignKey('galerie.nazwa'))
    artysta = db.relationship('Artysci', backref='eksponaty')
    galeria = db.relationship('Galerie', backref='eksponaty')


class Historia(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    eksponat_tytul = db.Column(db.Text, db.ForeignKey('eksponaty.tytul'), nullable=False)
    galeria_nazwa = db.Column(db.Text, db.ForeignKey('galerie.nazwa'), nullable=False)
    poczatek = db.Column(db.Date, nullable=False)
    koniec = db.Column(db.Date)
    eksponat = db.relationship('Eksponaty', backref='historia')
    galeria = db.relationship('Galerie', backref='historia')


class Uzytkownicy(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(100))
    haslo = db.Column(db.String(100))
