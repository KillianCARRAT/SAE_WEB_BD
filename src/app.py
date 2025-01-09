from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5

import os.path


app = Flask(__name__)

def mkpath(p):
    return os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            p))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + mkpath('../testdb.db'))
app.url_map.strict_slashes = False
app.config['SECRET_KEY'] = 'e9767196-4490-415a-8d42-1b16d2ad2a24'
app.config['SECURITY_DEFAULT_REMEMBER_ME'] = False
app.config['SECURITY_REGISTERABLE'] = False
app.config['SECURITY_RECOVERABLE'] = False
app.config['SECURITY_TRACKABLE'] = False
app.config['SECURITY_CONFIRMABLE'] = False
app.config['SECURITY_CHANGEABLE'] = False
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)

from src.models.Utilisateur import Utilisateur
from src.models.Role import Role


@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(int(user_id))