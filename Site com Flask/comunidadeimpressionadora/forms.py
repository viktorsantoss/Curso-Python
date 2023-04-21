from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import InputRequired, EqualTo, Length, Email
from comunidadeimpressionadora.models import Usuario
from email_validator import validate_email, EmailNotValidError
from flask_login import current_user


class FormCriarConta(FlaskForm):
    # verificar se o e-mail já existe na base de dados
    def validate_email_custom(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email Cadastrado. Faça Login ou cadastre outro usuário')
        try:
            v = validate_email(email.data)  # validating the email
            email.data = v["email"]  # update with the normalized form
        except EmailNotValidError as e:
            raise ValidationError("Endereço de email inválido")

    username = StringField('Usuario', validators=[InputRequired()],
                           render_kw={'placeholder': 'Digite o seu nome de usuário'})
    email = StringField('E-mail', validators=[InputRequired(), validate_email_custom], render_kw={'placeholder': 'Digite o seu e-mail'})
    senha = PasswordField('Senha', validators=[InputRequired(), Length(6, 20)],
                          render_kw={'placeholder': 'Digite a sua senha'})
    confirmacao_senha = PasswordField('Confirmação de senha', validators=[InputRequired(),
                          EqualTo('senha', message='Campo tem que ser igual ao da senha')],
                          render_kw={'placeholder': 'Confirme a sua senha'})
    botao_submit_criarconta = SubmitField('Criar Conta')


class FormLogin(FlaskForm):
    email_login = StringField('E-mail', validators=[InputRequired(), Email()], render_kw={'placeholder': 'Digite o e-mail'})
    senha_login = PasswordField('Senha', validators=[InputRequired(), Length(6, 20)], render_kw={'placeholder': 'Senha'})
    relembrar_acesso = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):

    def validate_email_custom(self, email):
        try:
            v = validate_email(email.data)  # validating the email
            email.data = v["email"]  # update with the normalized form
        except EmailNotValidError as e:
            raise ValidationError("Endereço de email inválido")
        else:
            if current_user.email != email.data:
                usuario = Usuario.query.filter_by(email=email.data).first()
                if usuario:
                    raise ValidationError('Email Já existe. digite outro e-mail')

    username = StringField('Usuario', validators=[InputRequired()],
                           render_kw={'placeholder': 'Digite um novo nome do usuário'})
    email = StringField('Email', validators=[InputRequired(), validate_email_custom],
                        render_kw={'placeholder': 'Digite um novo e-mail'})
    foto_perfil = FileField('Editar foto do perfil', validators=[FileAllowed(['jpg', 'png'],
                                                    message='meu ovo. Somente arquivo png e jpg')])
    botao_submit_alterar = SubmitField('Fazer alteração')
    curso_excel = BooleanField('Excel Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_vba = BooleanField('VBA Impresionador')
    curso_sql = BooleanField('SQL Impressionador')
    curso_pb = BooleanField('Power BI Impressioandor')
    curso_power_point = BooleanField('Apresentação Impressionador')


class FormPost(FlaskForm):
    titulo = StringField('Titulo do Post', validators=[InputRequired()])
    corpo = TextAreaField('Corpo do Post', validators=[InputRequired()])
    botao_post = SubmitField('Criar Post')