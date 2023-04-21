from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '2d40aff4995edd0c66a564dcefdda606'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidadeimpressionadora.db'
bcrypt = Bcrypt(app)
database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message ='Faça login para continuar'
login_manager.login_message_category = 'alert-info'

from comunidadeimpressionadora import routes