# This is making the app folder into a python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__) # the name of the file
    app.config['SECRET_KEY'] = 'dasncuas sdanodmas'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    from .views import main
    from .auth import auth

    app.register_blueprint(main, urlprefix="/")
    app.register_blueprint(auth, urlprefix="/")

    from . import models
    
    create_database(app=app)

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        with app.app_context():
            db.create_all()