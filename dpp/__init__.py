import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    """ 
    app.config.from_mapping(
        SECRET_KEY='_secret_',
        SQLALCHEMY_DATABASE_URI= f"sqlite:///{os.path.join(app.instance_path, '/database/dpp.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    ) """
    
    Bootstrap(app)

    if test_config is None:
        app.config.from_object('config.Config')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path + '/database')
    except OSError:
        pass
    


    @app.route('/hello')
    def hello():
        return "Hello, it is a beautifull world, isn't it?"
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = 'You msut be logged in.'
    login_manager.blueprint_login_views = {
        'auth' : 'auth.login',
        'admin' : 'admin.login'
    }
    migrate.init_app(app, db)
    mail.init_app(app)

    from . import models

    from .admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from .auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from .home import home
    app.register_blueprint(home)

    return app
