import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import Note, List, Task
from __init__ import db


#define urls with blueprint
views = Blueprint('views', __name__)

#adding notes
@views.route('/', methods=['GET', 'POST'])
#decoretor to check if user is logged in
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Please write a note before add it to your MindMe', category='error')
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

#Todo Lists and tasks

#retrieve and add lists
@views.route('/todo', methods=['GET', 'POST'])
#decoretor to check if user is logged in
@login_required
def todo():
    if request.method == 'POST':
        list = request.form.get('list')

        if len(list) < 1:
            flash('Please write a list before add it to your MindMe', category='error')
        else:
            new_list = List(list=list, user_id=current_user.id)
            db.session.add(new_list)
            db.session.commit()

            flash('List added! :)')

    return render_template("todo.html", user=current_user)

#delete list
@views.route('/delete-list/<list_id>', methods=['POST'])
@login_required
def delete_list(list_id):
    list_ = List.query.get(list_id)
    if list_ and list_.user_id == current_user.id:  # Verify the list belongs to the current user
        # Optionally delete tasks associated with the list
        Task.query.filter_by(list_id=list_.id).delete()
        db.session.delete(list_)
        db.session.commit()
        flash('List deleted!', category='success')
    else:
        flash('List not found or unauthorized action!', category='error')

    return redirect(url_for('views.todo'))

#update list
@views.route('/update-list/<list_id>', methods=['POST'])
@login_required
def update_list(list_id):
    list_ = List.query.get(list_id)
    if list_ and list_.user_id == current_user.id:  # Verify ownership
        new_list_name = request.form.get('new_list_name')
        if len(new_list_name) < 1:
            flash('List name cannot be empty!', category='error')
        else:
            list_.list = new_list_name
            db.session.commit()
            flash('List updated!', category='success')
    else:
        flash('List not found or unauthorized action!', category='error')

    return redirect(url_for('views.todo'))


#retrieve and add tasks
@views.route('/todo/<list_id>', methods=['GET', 'POST'])
@login_required
def tasks(list_id):
    # Retrieve the list by ID
    list_ = List.query.get(list_id)
    if not list_:
        flash('List not found!', category='error')
        return redirect(url_for('views.todo'))

    if request.method == 'POST':
        task = request.form.get('task')
        if len(task) < 1:
            flash('Please write a task before adding it to your MindMe', category='error')
        else:
            new_task = Task(task=task, list_id=list_.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Task added! :)')

    return render_template("tasks.html", user=current_user, list=list_)

#delete task
@views.route('/delete-task/<task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    # Retrieve the task by ID
    task = Task.query.get(task_id)
    if task: 
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!', category='success')
    else:
        flash('Task not found or unauthorized action!', category='error')

    return redirect(request.referrer or url_for('views.todo'))

#update task
@views.route('/update-task/<task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task: 
        new_task_content = request.form.get('new_task_content')
        if len(new_task_content) < 1:
            flash('Task content cannot be empty!', category='error')
        else:
            task.task = new_task_content
            db.session.commit()
            flash('Task updated!', category='success')
    else:
        flash('Task not found or unauthorized action!', category='error')

    return redirect(request.referrer or url_for('views.todo'))






