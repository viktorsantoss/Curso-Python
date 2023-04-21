from comunidadeimpressionadora import app, database, bcrypt
from flask import render_template, url_for, request, redirect, flash, abort
from comunidadeimpressionadora.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormPost
from comunidadeimpressionadora.models import Usuario, Post
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image




@app.route("/")
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contatos')
def contato():
    return render_template('contatos.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuario.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['post', 'get'])
def login():
    form_criarconta = FormCriarConta()
    form_login = FormLogin()
    if 'botao_submit_login' in request.form and form_login.validate_on_submit():
        with app.app_context():
            usuario = Usuario.query.filter_by(email=form_login.email_login.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha_login.data):
            login_user(usuario, remember=form_login.relembrar_acesso.data)
            flash(f'Login Realizado com sucesso para o e-mail {form_login.email_login.data}', 'alert-success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Email ou Senha inválido.', 'alert-danger')
    if 'botao_submit_criarconta' in request.form and form_criarconta.validate_on_submit():
        senha_encriptada = bcrypt.generate_password_hash(form_criarconta.senha.data)
        with app.app_context():
            usuario = Usuario(senha=senha_encriptada, email=form_criarconta.email.data, username=form_criarconta.username.data)
            database.session.add(usuario)
            database.session.commit()

        flash(f'Login Realizado com sucesso para o e-mail {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/post/criar', methods=['POST', 'GET'])
@login_required
def criar_post():
    form = FormPost()

    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('post.html', form=form)


@app.route('/perfil')
@login_required
def meu_perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


def alterar_foto(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    novo_nome = nome + codigo + extensao
    caminho = os.path.join(app.root_path, 'static/fotos_perfil', novo_nome)
    tamanho = (400, 400)
    nova_imagem = Image.open(imagem)
    nova_imagem.thumbnail(tamanho)
    nova_imagem.save(caminho)
    return novo_nome


def atualizar_curso(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name and campo.data:
            lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        with app.app_context():
            current_user.username = form.username.data
            current_user.email = form.email.data
            if form.foto_perfil.data:
                nova_imagem = alterar_foto(form.foto_perfil.data)
                current_user.foto_perfil = nova_imagem
            current_user.curso = atualizar_curso(form)
            database.session.commit()
        flash('Alterações realizadas com sucesso', 'alert-success')
        return redirect(url_for('meu_perfil'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_perfil}')
    return render_template('editar_perfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<id_post>', methods=['GET', 'POST'])
@login_required
def exibir_post(id_post):
    post = Post.query.get(id_post)
    if current_user == post.autor:
        form = FormPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post alterado com sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('exibir_post.html', post=post, form=form)


@app.route('/post/<id_post>/ecluir', methods=['GET', 'POST'])
def excluir(id_post):
    post = Post.query.get(id_post)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)
