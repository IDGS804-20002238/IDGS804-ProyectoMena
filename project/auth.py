from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import User
from . import db, userDataStore
auth = Blueprint('auth', __name__, url_prefix='/security')
@auth.route('/login')
def login():
    return render_template('/security/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('El usuario y/o la contraseña son incorrectos')
        return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, password):
        flash('El usuario y/o la contraseña son incorrectos')
        return redirect(url_for('auth.login'))
    
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/register')
def register():
    return render_template('/security/register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # recuperar el primer elemento de la lista

    if user:
        flash('El correo electrónico ya existe')
        return redirect(url_for('auth.register'))

    new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'), idrole='4')
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))



@auth.route('/logout')
@login_required
def logout():
    
    logout_user()
    return redirect(url_for('main.index'))