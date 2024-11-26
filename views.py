import json
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from models import Note
from __init__ import db


#define urls with blueprint
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
#decoretor to check if user is logged in
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Please write a note before add it your MindMe', category='error')
        else:
            new_note = Note(note=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash('Note added! :)')

    return render_template("index.html", user=current_user)

#for deleting notes

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    #taking the data from post request and load as json object
    note = json.loads(request.data)
    #access to noteId attribute that is in index.js
    noteId = note['noteId']
    #look for the note with that id
    note = Note.query.get(noteId)
    #check if the note exist
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



