from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
db = SQLAlchemy()


def create_app():
    from .models import Uzytkownicy
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint

    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres@localhost/muzeum_db'
    # app.debug = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Uzytkownicy.query.get(int(user_id))

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    return app
