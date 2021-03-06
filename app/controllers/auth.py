# Rotas com identificação
# ----------------------
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.models.models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('logar.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or  not check_password_hash(user.password, password):
        flash('Dados incorretos')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('main.grupos'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    db.create_all()

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    telefone = request.form.get('telefone')

    # Retorna ao usuario se o email já existe
    user = User.query.filter_by(email=email).first()

    if user:
        flash('E-mail já cadastrado')
        return redirect(url_for('auth.signup'))
    
    #Criando novo usuário
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), telefone=telefone)

    # Adicionando o usuário ao banco de dados
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

    


