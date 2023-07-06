# This is making the app folder into a python package

from flask import Flask

def create_app():
    app = Flask(__name__) # the name of the file
    app.config['SECRET_KEY'] = 'dasncuas sdanodmas'
    
    return app