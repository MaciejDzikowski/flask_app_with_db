from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, login_required
from .models import Uzytkownicy


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')

    user = Uzytkownicy.query.filter_by(nazwa=name).first()

    if not user:
        return render_template('login.html', error="Uzytkownik nie istnieje!")
    if not user.haslo == password:
        return render_template('login.html', error="Niepoprawne haslo")  # ze wzgledow bezp raczej nie powinno sie udostepiac informacji, co poszlo zle

    login_user(user)
    flash("Witaj, {}!".format(user.nazwa))
    return redirect(url_for('main.profile'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
