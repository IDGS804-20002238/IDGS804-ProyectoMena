from flask import Blueprint, render_template, redirect, url_for, request, flash,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_security import login_required
from flask_security.utils import login_user, logout_user, hash_password, encrypt_password
from . models import User, Domicilio
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

@auth.route('/registerU', methods=['GET', 'POST'])
def register_post():
    email = request.get_json()['email']
    name = request.get_json()['name']
    password = request.get_json()['password']

    user = User.query.filter_by(email=email).first()

    if user:
        response = {'status': 'error', 'message': 'el correo ya existe'}
        return jsonify(response)
    
    # obtiene los datos del form para llenar la tabla domicilio
    estado = request.get_json()['estado']
    municipio = request.get_json()['municipio']
    codigoPostal = request.get_json()['codigoPostal']
    colonia = request.get_json()['colonia']
    calle = request.get_json()['calle']
    numeroInt = request.get_json()['numeroInt']
    numeroExt = request.get_json()['numeroExt']
    referencia = request.get_json()['referencia']

    #inserta el domicilio
    domicilio = Domicilio(estado=estado, municipio=municipio, codigoPostal=codigoPostal, colonia=colonia, calle=calle, numeroInt=numeroInt, numeroExt=numeroExt, referencia=referencia)
    db.session.add(domicilio)
    db.session.commit()

    # obtiene el id del domicilio recién insertado
    domicilio_id = domicilio.domicilioId

    # crea un nuevo objeto User y agrega el id del domicilio a la columna domicilioId
    new_user = User(name=name, email=email, password=generate_password_hash(password, method='sha256'), idrole='4', domicilioId=domicilio_id)
    db.session.add(new_user)
    db.session.commit()

    response = {'status': 'success', 'message': 'La compra se ha actualizado correctamente'}
    return jsonify(response)




@auth.route('/logout')
@login_required
def logout():
    
    logout_user()
    return redirect(url_for('main.index'))