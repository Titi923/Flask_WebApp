from flask import Blueprint, render_template, request, Flask, flash, jsonify, redirect
import os, json, datetime
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import Image, Note
from sqlalchemy.sql import func


main = Blueprint('main', __name__)


# @main.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == 'POST':
#         print(request.form.get('file'))
#     return render_template("home.html", user=current_user)

@main.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # pass
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     new_note = Note(data=note, user_id=current_user.id)
    #     db.session.add(new_note)
    #     db.session.commit()

    # return render_template('home.html', user=current_user)


    if request.method == 'POST':
        upload()
    images = Image.query.filter_by(user_id=current_user.id).all()

    return render_template('home.html', user=current_user, images=images)
    
@main.route('/pdf-edit', methods=['GET', 'POST'])
@login_required
def pdfedit():
    pass
    # return render_template('pdfEdit/pdfedit.html', user=current_user)
   
    
# UPDATE Note
@main.route('/update-note/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    note_to_update = Note.query.get_or_404(id)
    if request.method == 'POST':
        try:
            note_to_update.data = request.form['note_data']
            note_to_update.date = func.now()
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating that note"
    return render_template('update.html', note_to_update=note_to_update, user=current_user)

# DELETE Note
@main.route('/delete-note/<int:id>')
@login_required
def delete_note(id):  
    note_to_delete = Note.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that note"

# UPLOAD Image
@main.route('/upload', methods=['GET', 'POST'])
def upload():
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    
    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    file = request.files['file']
    if file and allowed_file(file.filename):
        user_id = current_user.id

        # Generate a unique filename based on the user's ID
        filename = f'user_{user_id}_{secure_filename(file.filename)}'
                
        # filename = file.filename
        file_path = os.path.join(Flask(__name__).root_path, 'static/images', filename)
        file.save(file_path)
        flash('File uploaded successfully.', category='success')

        # Create a new Image instance and associate it with the current user
        image = Image(filename=filename, user_id=current_user.id, filepath=file_path)
        db.session.add(image)
        db.session.commit()

    else:
        return 'No file selected or you did not uploaded an image format'


# DELETE Image
@main.route('/delete-image/<int:id>')
@login_required
def delete_image(id):  
    image_to_delete = Image.query.get_or_404(id)

    try:
        db.session.delete(image_to_delete)
        db.session.commit()

        os.remove(image_to_delete.filepath)
        return redirect('/')
    except:
        return "There was a problem deleting that note"


