from . import db
from .models import Eksponaty, Artysci, Historia, Galerie
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import SelectField
from sqlalchemy.exc import IntegrityError
from datetime import date


main = Blueprint('main', __name__)


class Form(FlaskForm):
    authors = SelectField('authors', choices=[])
    galleries = SelectField('galleries', choices=[])
    exhibits = SelectField('exhibits', choices=[])


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/found_exhibits', methods=['GET', 'POST'])
def find_exhibit():
    title = request.form.get('title')
    author = request.form.get('author')
    etype = request.form.get('etype')
    date = request.form.get('date')

    if title and author and etype:
        qry = Eksponaty.query.filter_by(tytul=title).filter_by(typ=etype).join(Artysci).filter_by(nazwisko=author)
    elif title and author:
        qry = Eksponaty.query.filter_by(tytul=title).join(Artysci).filter_by(nazwisko=author)
    elif title and etype:
        qry = Eksponaty.query.filter_by(tytul=title).filter_by(typ=etype)
    elif author and etype:
        qry = Eksponaty.query.filter_by(typ=etype).join(Artysci).filter_by(nazwisko=author)
    elif title:
        qry = Eksponaty.query.filter_by(tytul=title)
    elif author:
        qry = Eksponaty.query.join(Artysci).filter_by(nazwisko=author)
    elif etype:
        qry = Eksponaty.query.filter_by(typ=etype)
    else:
        qry = Eksponaty.query
    exhibits = [item for item in qry.all()]

    if not exhibits:
        return render_template('index.html', msg="Nic nie znaleziono. Sprobuj ponownie.")
    else:
        if date:
            past_locs = []
            for exhibit in exhibits:
                if [item for item in Historia.query.filter_by(eksponat=exhibit).filter(
                        Historia.poczatek < date, date < Historia.koniec).all()]:
                    past_locs += Historia.query.filter_by(eksponat=exhibit).filter(
                        Historia.poczatek < date, date < Historia.koniec).all()
                elif [item for item in Historia.query.filter_by(eksponat=exhibit).filter(
                        Historia.poczatek < date, Historia.koniec.is_(None)).all()]:
                    past_locs += Historia.query.filter_by(eksponat=exhibit).filter(
                        Historia.poczatek < date, Historia.koniec.is_(None)).all()
                else:
                    past_locs.append(None)
            zipped = zip(exhibits, past_locs)
            return render_template('found_exhibits.html', exhibits=zipped, date=date)
        else:
            return render_template('found_exhibits.html', exhibits=exhibits, date=False)


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.nazwa)


@main.route('/new')
@login_required
def new():
    return render_template('new.html')


@main.route('/new', methods=['POST'])
@login_required
def new_post():
    choice = request.form.get('choice')
    if choice == "exhibit":
        return redirect(url_for('main.new_exhibit'))
    else:
        return redirect(url_for('main.new_artist'))


@main.route('/new_exhibit')
@login_required
def new_exhibit():
    form = Form()
    form.authors.choices = ['brak'] + [author.nazwisko for author in Artysci.query.all()]
    form.galleries.choices = ['brak'] + [gallery.nazwa for gallery in Galerie.query.all()]
    return render_template('new_exhibit.html', form=form)


@main.route('/new_exhibit', methods=['POST'])
@login_required
def new_exhibit_post():
    title = request.form.get('title')
    etype = request.form.get('etype')
    height = request.form.get('height')
    width = request.form.get('width')
    author = Artysci.query.filter_by(nazwisko=request.form.get('authors')).first()
    gallery = Galerie.query.filter_by(nazwa=request.form.get('galleries')).first()

    exhibit = Eksponaty(tytul=title, typ=etype, wysokosc=height, szerokosc=width, artysta=author, galeria=gallery)
    db.session.add(exhibit)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('Eksponat o podanym tytule juz instnieje! Sprobuj ponownie.')
        return redirect(url_for('main.new_exhibit'))

    flash('Dodano eksponat!')
    return redirect(url_for('main.new_exhibit'))


@main.route('/new_artist')
@login_required
def new_artist():
    form = Form()
    form.galleries.choices = ['brak'] + [gallery.nazwa for gallery in Galerie.query.all()]
    return render_template('new_artist.html', form=form)


@main.route('/new_artist', methods=['POST'])
@login_required
def new_artist_post():
    name = request.form.get('name')
    birth_year = request.form.get('birth_year')
    death_year = request.form.get('death_year')
    if int(birth_year) >= int(death_year):
        flash('Rok smierci nie moze byc wczesniejszy niz rok urodzenia! Sprobuj ponownie.')
        return redirect(url_for('main.new_artist'))

    artist = Artysci(nazwisko=name, rok_urodzenia=birth_year, rok_smierci=death_year)
    db.session.add(artist)

    title = request.form.get('title')
    etype = request.form.get('etype')
    height = request.form.get('height')
    width = request.form.get('width')
    author = artist
    gallery = Galerie.query.filter_by(nazwa=request.form.get('galleries')).first()

    exhibit = Eksponaty(tytul=title, typ=etype, wysokosc=height, szerokosc=width, artysta=author, galeria=gallery)
    db.session.add(exhibit)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash('Artysta o podanym nazwisku lub eksponat o podanym tytule juz instnieje! Sprobuj ponownie.')
        return redirect(url_for('main.new_artist'))

    flash('Dodano artyste i jego pierwsze dzielo!')
    return redirect(url_for('main.new_artist'))


@main.route('/history')
@login_required
def history():
    form = Form()
    form.exhibits.choices = [exhibit.tytul for exhibit in Eksponaty.query.all()]
    return render_template('history.html', form=form)


@main.route('/found_history', methods=['POST'])
@login_required
def history_post():
    exhibit = Eksponaty.query.filter_by(tytul=request.form.get('exhibits')).first()
    history_records = [item for item in Historia.query.filter_by(eksponat=exhibit).all()]
    return render_template('found_history.html', history_records=history_records, exhibit=exhibit.tytul)


@main.route('/edit_loc')
@login_required
def edit_loc():
    form = Form()
    form.exhibits.choices = [exhibit.tytul for exhibit in Eksponaty.query.all()]
    form.galleries.choices = ['Magazyn'] + [gallery.nazwa for gallery in Galerie.query.all()]
    return render_template('edit_loc.html', form=form)


@main.route('/edit_loc', methods=['POST'])
@login_required
def edit_loc_post():
    exhibit = Eksponaty.query.filter_by(tytul=request.form.get('exhibits')).first()
    gallery = Galerie.query.filter_by(nazwa=request.form.get('galleries')).first()

    history_record = Historia.query.filter_by(eksponat=exhibit).filter(Historia.koniec.is_(None)).first()
    today = date.today()

    if exhibit.galeria != gallery:
        exhibit.galeria = gallery
    else:
        flash('Eksponat juz znajduje sie w tej lokalizacji! Sprobuj ponownie.')
        return redirect(url_for('main.edit_loc'))

    if history_record:
        history_record.koniec = today

    if gallery:
        new_record = Historia(eksponat=exhibit, galeria=gallery, poczatek=today, koniec=None)
        db.session.add(new_record)

    try:
        db.session.commit()
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        flash('Cos poszlo nie tak. Sprobuj ponownie.')
        return redirect(url_for('main.edit_loc'))

    flash('Przeniesiono eksponat.')
    return redirect(url_for('main.edit_loc'))


@main.route('/erd')
@login_required
def erd():
    return render_template('erd.html')


@main.route('/script')
@login_required
def script():
    return render_template('script.html')
