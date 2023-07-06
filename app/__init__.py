# This is making the app folder into a python package

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
    
    return app