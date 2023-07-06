from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", isLoggedIn=False)

@auth.route('/logout')
def logout():
    return "<h1>Logged out</h1>"

@auth.route('/sign-up')
def signup():
    if request.form == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        

    return render_template("signUp.html", methods=['GET', 'POST'])