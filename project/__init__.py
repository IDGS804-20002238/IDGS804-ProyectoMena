from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
from .models import User, Role
#Creamos un objeto de la clase SQLAlchemyUserDatastore
userDataStore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://angel:root@127.0.0.1/mena'
    app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
    app.config['SECURITY_PASSWORD_SALT'] = 'thisissecretsalt'


    db.init_app(app)
    @app.before_first_request
    def create_all():
        db.create_all()


    security = Security(app, userDataStore)

  


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .productos import productos as main_blueprint
    app.register_blueprint(main_blueprint)


    return app
