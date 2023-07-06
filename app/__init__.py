# This is making the app folder into a python package

from flask import Flask

def create_app():
    app = Flask(__name__) # the name of the file
    app.config['SECRET_KEY'] = 'dasncuas sdanodmas'
    
    from .views import views
    from .auth import auth

    app.register_blueprint(views, urlprefix="/")
    app.register_blueprint(auth, urlprefix="/")
    
    return app