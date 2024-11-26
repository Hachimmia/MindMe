from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
database = "database.db"


def create_app():
    #flask app
    app = Flask(__name__)
    #cache
    app.config['SECRET_KEY'] = 'hello123'
    #database
    #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:/{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)

    #import variables
    from views import views
    from auth import auth

    #how access views and auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User, Note

    create_database(app)

    login_manager = LoginManager()
    #where to be redirected if the user is not logeed in
    login_manager.login_view = 'auth.login'
    #it tells to the login manager with app we are using
    login_manager.init_app(app)

    #tell to flask how we load the user
    @login_manager.user_loader
    def load_user(id):
        #say what user we are looking for
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('/'+ database):
         with app.app_context():
             db.create_all()
             print ("db created")