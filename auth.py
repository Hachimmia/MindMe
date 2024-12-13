from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db

#define urls with blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        #check email and passoword of users
        user = User.query.filter_by(email=email).first()
        if user: 
            if check_password_hash(user.password, password):
                flash('logged in successfully!', category='success')
                #using flask_login to remember session of user
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else: 
                flash('incorrect password, try again', category='error')
        else:
    #if the user doesn't exist
            flash('Your account doesn\'t exist, please Sign up to MindMe', category='error')

    #this var it has info about the request of this route
    #data = request.form
    #print(data)
    #Var text can be access from login.html
    #return render_template("login.html", test="Testing")
    return render_template("login.html", user=current_user)


@auth.route('/logout')
#makes sure that the user can access only if they are logged in
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        passconfirm = request.form.get('passconfirm')

        user = User.query.filter_by(email=email).first()
        if user: 
            flash('This email is already used by another user', category='error')
        elif len(email) < 5:
            #message using flash
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password != passconfirm:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            #add user to db
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)