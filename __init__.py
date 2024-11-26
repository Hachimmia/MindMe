from flask import Flask

def create_app():
    app = Flask(__name__)
    #cache
    app.config['SECRET_KEY'] = 'hello123'

    #import variables
    from views import views
    from auth import auth

    #how access views and auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app