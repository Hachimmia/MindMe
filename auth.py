from flask import Blueprint, render_template, request, flash

#define urls with blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    #this var it has info about the request of this route
    #data = request.form
    #print(data)
    #Var text can be access from login.html
    #return render_template("login.html", test="Testing")
    return render_template("login.html")


@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        passconfirm = request.form.get('passconfirm')

        if len(email) < 5:
            #message using flash
            flash('Email must be greater than 4 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password != passconfirm:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', category='error')
        else:
            flash('Account created!', category='success')
            #add user to db

    return render_template("signup.html")