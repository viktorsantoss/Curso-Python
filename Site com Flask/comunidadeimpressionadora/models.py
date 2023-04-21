from comunidadeimpressionadora import database
from datetime import datetime
from comunidadeimpressionadora import login_manager
from flask_login import UserMixin


@login_manager.user_loader
def user_load(id_usuario):
    return Usuario.query.get(id_usuario)


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil= database.Column(database.String, default='default.jpg')
    curso = database.Column(database.String, default='Não informado')
    posts = database.relationship('Post', backref='autor', lazy=True)

    def contar_post(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)